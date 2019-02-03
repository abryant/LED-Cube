from display import Colour
from queue import Queue, Empty
import time
import generators
from interactive import draw, snake, write, interactive_autoscroll, spectrogram, rhythm
from visuals import corners, cube_visuals, edges, extend, faces, fireworks, flash, flatten, layers, line, matrix, pulse, rainbow, rope, rotate, shuffle, snakes, spiral, starfield, tetris, text, wave

GENERATORS = {
  'corners': corners.corners,
  'demo': cube_visuals.cube_visuals,
  'edges': edges.edges,
  'extend': extend.extend,
  'faces': faces.faces,
  'fireworks': fireworks.fireworks,
  'flash': flash.flash,
  'flatten': flatten.flatten,
  'layers': lambda: generators.slow(layers.layers(), frames = 4),
  'line': line.scrolling_rainbow,
  'matrix': matrix.matrix,
  'pulse': pulse.pulse,
  'rainbow': rainbow.scroll_diagonal_rainbow,
  'rope': rope.rope,
  'rotate': rotate.rotate,
  'shuffle': shuffle.shuffle,
  'snakes': snakes.snakes,
  'spiral': spiral.spiral,
  'starfield': starfield.starfield,
  'tetris': tetris.tetris,
  'text': lambda: text.text("COLOUR ", [Colour.red(), Colour.green(), Colour.blue()]),
  'wave': wave.wave,
}

INTERACTIVE_GENERATORS = {
  'rhythm': rhythm.Rhythm,
  'draw': draw.Draw,
  'snake': snake.Snake,
  'spectrogram': spectrogram.Spectrogram,
  'write': write.Write,
  'interactive_autoscroll': interactive_autoscroll.Autoscroll,
}

class Controller:
  def __init__(self, queue, file):
    self.queue = queue
    self.file = file
    self.brightness = 0.2
    self.delay = 0.05
    self.current_interactive = None
    self.current_visual = None
    self.stopped = False
    self.listeners = []

  def send(self, data):
    if type(data) is str:
      data = bytes(data, encoding="UTF-8")
    self.file.write(data)
    self.file.flush()

  def control_cube(self):
    try:
      self.send('Controlling...\n')
      while not self.stopped:
        if self.current_interactive is not None:
          try:
            result = next(self.current_interactive.generator)
            frame = generators.get_colours(result.value)
            if type(frame) is list:
              self.send_frame(frame)
            t = time.perf_counter()
            start_time = t
            while (not self.stopped
                   and (self.current_interactive is not None)
                   and (not result.wait_for_input or not self.current_interactive.has_input())
                   and (result.timeout is None or t < start_time + result.timeout)):
              try:
                timeout = None
                if result.timeout is not None:
                  timeout = result.timeout - (t - start_time)
                if timeout is None or timeout > 60:
                  timeout = 60
                entry = self.queue.get(timeout = timeout)
                old_interactive = self.current_interactive
                self.process_command(entry)
                if self.current_interactive is not old_interactive:
                  break
              except Empty:
                # Send a blank line whenever we time out, to stop the connection from dropping
                self.send(b'\n')
              t = time.perf_counter()
          except StopIteration:
            self.current_interactive = None
        elif self.current_visual is not None:
          self.send_visual_frame()
          t = time.perf_counter()
          self.last_frame_time = t
          while (not self.stopped
                 and (self.current_visual is not None)
                 and (t < self.last_frame_time + self.delay)):
            try:
              entry = self.queue.get(timeout = self.delay - (t - self.last_frame_time))
              self.process_command(entry)
            except Empty:
              pass
            t = time.perf_counter()
        else:
          try:
            entry = self.queue.get(timeout = 60)
            self.process_command(entry)
          except Empty:
            # Send a blank line whenever we time out, to stop the connection from dropping.
            self.send(b'\n')
    finally:
      for l in self.listeners:
        l.put(b'quit')

  def send_visual_frame(self):
    try:
      while True:
        frame = next(self.current_visual)
        frame = generators.get_colours(frame)
        if type(frame) is list:
          self.send_frame(frame)
          return
    except StopIteration:
      self.current_visual = None

  def send_frame(self, frame):
    frame_bytes = bytes([b for c in frame for b in [c.r, c.g, c.b]])
    scaled_brightness_bytes = bytes([int(b * self.brightness) for b in frame_bytes])
    data_scaled = b'CUBE:' + bytes([len(frame) >> 8, len(frame) & 0xff]) + scaled_brightness_bytes + b'\n'
    data_unscaled = b'CUBE:' + bytes([len(frame) >> 8, len(frame) & 0xff]) + frame_bytes + b'\n'
    self.send(data_scaled)
    for l in self.listeners:
      l.put(data_unscaled)


  def process_command(self, entry):
    command = entry['command']
    if command == 'quit':
      self.send('Quitting...\n')
      for l in self.listeners:
        l.put(b'quit')
      self.stopped = True
      return
    if command == 'listen':
      self.listeners.append(entry['data_queue'])
      return
    if command.startswith('delay=') and len(command) > len('delay='):
      try:
        d = float(command[len('delay='):])
        if d >= 0.015:
          self.delay = d
      except ValueError:
        pass
      return
    if command.startswith('brightness=') and len(command) > len('brightness='):
      try:
        b = float(command[len('brightness='):])
        if b >= 0 and b <= 1:
          self.brightness = b
      except ValueError:
        pass
      return
    if command.startswith('input:'):
      data = command[len('input:'):]
      if self.current_interactive is not None:
        self.current_interactive.add_input(data)
      return
    if command.startswith('start:'):
      name = command[len('start:'):].lower()
      if name in GENERATORS:
        self.current_interactive = None
        self.current_visual = GENERATORS[name]()
      elif name in INTERACTIVE_GENERATORS:
        self.current_interactive = INTERACTIVE_GENERATORS[name]()
        self.current_visual = None
      return
    if command == 'stop':
      self.current_interactive = None
      self.current_visual = None
      return


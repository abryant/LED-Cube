from display import Colour
from queue import Queue, Empty
from time import sleep
import generators
from visuals import corners, cube_visuals, extend, flash, flatten, line, matrix, pulse, rainbow, rotate, shuffle, sides, snakes, tetris

GENERATORS = {
  'corners': corners.corners,
  'demo': cube_visuals.cube_visuals,
  'extend': extend.extend,
  'flash': flash.flash,
  'flatten': flatten.flatten,
  'line': line.scrolling_rainbow,
  'matrix': matrix.matrix,
  'pulse': pulse.pulse,
  'rainbow': rainbow.scroll_diagonal_rainbow,
  'rotate': rotate.rotate,
  'shuffle': shuffle.shuffle,
  'sides': sides.sides,
  'snakes': lambda: generators.slow(snakes.snakes()),
  'tetris': tetris.tetris,
}

class Controller:
  def __init__(self, queue, file):
    self.queue = queue
    self.file = file
    self.delay = 0.05
    self.current_generator = None
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
      while True:
        if self.current_generator is None:
          try:
            entry = self.queue.get(timeout = 60)
            self.process_command(entry)
          except Empty:
            # Send a blank line whenever we time out, to stop the connection from dropping.
            self.send(b'\n')
        else:
          try:
            entry = self.queue.get_nowait()
            self.process_command(entry)
          except Empty:
            pass
        if self.stopped:
          return
        if self.current_generator is not None:
          self.send_frame()
          sleep(self.delay)
    finally:
      for l in self.listeners:
        l.put(b'quit')

  def send_frame(self):
    try:
      while True:
        frame = next(self.current_generator)
        frame = generators.get_colours(frame)
        if type(frame) is list:
          frame_bytes = bytes([b for c in frame for b in [c.r, c.g, c.b]])
          data = b'CUBE:' + bytes([len(frame) >> 8, len(frame) & 0xff]) + frame_bytes + b'\n'
          self.send(data)
          for l in self.listeners:
            l.put(data)
          return
    except StopIteration:
      self.current_generator = None

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
        b = int(command[len('brightness='):])
        if b >= 0 and b < 256:
          Colour.brightness = b
      except ValueError:
        pass
      return
    if command.startswith('start:'):
      name = command[len('start:'):].lower()
      if name in GENERATORS:
        self.current_generator = GENERATORS[name]()
      return
    if command == 'stop':
      self.current_generator = None
      return


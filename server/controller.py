from queue import Queue, Empty
from time import sleep
import generators
from visuals import corners, cube_visuals, extend, flash, flatten, matrix, pulse, rainbow, rotate, shuffle, sides, snakes, tetris

GENERATORS = {
  'corners': corners.corners,
  'cube_visuals': cube_visuals.cube_visuals,
  'extend': extend.extend,
  'flash': flash.flash,
  'flatten': flatten.flatten,
  'matrix': matrix.matrix,
  'pulse': pulse.pulse,
  'rainbow': rainbow.scroll_diagonal_rainbow,
  'rotate': rotate.rotate,
  'shuffle': shuffle.shuffle,
  'sides': sides.sides,
  'snakes': snakes.snakes,
  'tetris': tetris.tetris,
}

class Controller:
  def __init__(self, queue, file):
    self.queue = queue
    self.file = file
    self.delay = 0.05
    self.brightness = 50
    self.current_generator = None
    self.stopped = False

  def send(self, data):
    if type(data) is str:
      data = bytes(data, encoding="UTF-8")
    self.file.write(data)
    self.file.flush()

  def control_cube(self):
    self.send('Controlling...\n')
    while True:
      if self.current_generator is None:
        command = self.queue.get()
        self.process_command(command)
      else:
        try:
          command = self.queue.get_nowait()
          self.process_command(command)
        except Empty:
          pass
      if self.stopped:
        return
      if self.current_generator is not None:
        self.send_frame()
        sleep(self.delay)
      else:
        self.send('.\n')

  def send_frame(self):
    try:
      while True:
        frame = next(self.current_generator)
        frame = generators.get_colours(frame)
        if type(frame) is list:
          frame_bytes = bytes([b for c in frame for b in [c.r, c.g, c.b]])
          self.send(b'CUBE:' + bytes([len(frame) >> 8, len(frame) & 0xff]) + frame_bytes + b'\n')
          return
    except StopIteration:
      self.current_generator = None

  def process_command(self, command):
    if command == 'quit':
      self.send('Quitting...\n')
      self.stopped = True
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
          self.brightness = b
      except ValueError:
        pass
      return
    if command.startswith('start:'):
      name = command[len('start:'):]
      if name in GENERATORS:
        self.current_generator = GENERATORS[name]()
      return
    if command == 'stop':
      self.current_generator = None
      return


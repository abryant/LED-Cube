from queue import Queue, Empty
from time import sleep

def asdf():
  while True:
    yield 'a'
    yield 's'
    yield 'd'
    yield 'f'

class Controller:
  def __init__(self, queue, file):
    self.queue = queue
    self.file = file
    self.delay = 1
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
        self.send(next(self.current_generator) + '\n')
        sleep(self.delay)
      else:
        self.send('.\n')

  def process_command(self, command):
    if command == 'quit':
      self.send('Quitting...\n')
      self.stopped = True
      return
    if command.startswith('delay=') and len(command) > len('delay='):
      try:
        d = float(command[len('delay='):])
        if d > 0:
          self.delay = d
      except ValueError:
        pass
      return
    if command == 'asdf':
      self.current_generator = asdf()
      return
    if command == 'stop':
      self.current_generator = None
      return


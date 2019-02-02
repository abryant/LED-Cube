from queue import Queue, Empty
from visuals.position import *
import time

class InteractiveResponse:

  def __init__(self, value = None, timeout = None, wait_for_input = False):
    if timeout is None and not wait_for_input:
      raise "No continuation condition in interactive response"
    self.value = value
    self.timeout = timeout
    self.wait_for_input = wait_for_input

def wait_for_input(value = None):
  return InteractiveResponse(value = value, wait_for_input = True)

def wait_time(time, value = None):
  return InteractiveResponse(value = value, timeout = time)

def wait_for_input_or_time(time, value = None):
  return InteractiveResponse(value = value, timeout = time, wait_for_input = True)

DIRECTIONS = {
  'back': Direction.BACK,
  'left': Direction.LEFT,
  'front': Direction.FRONT,
  'right': Direction.RIGHT,
  'up': Direction.UP,
  'down': Direction.DOWN,
}


class Interactive:

  def __init__(self):
    self.input_queue = Queue()
    self.generator = self.run()

  def run(self):
    """A non-blocking generator function that yields InteractiveResponses"""
    pass

  def clear_input(self):
    while True:
      try:
        self.input_queue.get_nowait()
      except Empty:
        return

  def add_input(self, input):
    self.input_queue.put(input)

  def has_input(self):
    return not self.input_queue.empty()

  def get_input(self, options = None):
    """Consumes input until it reaches one of the options, or returns None if there is none."""
    while True:
      try:
        input = self.input_queue.get_nowait()
        if options is None:
          return input
        if input in options:
          return options[input]
      except Empty:
        return None

  def get_input_direction(self):
    return self.get_input(DIRECTIONS)


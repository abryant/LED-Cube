from grid import *
from display import *
import random
import generators
import functools

# Each transition is a generator that returns all of the frames in the
# transition, including the start and end frames passed to it.

def scroll(direction, start, end):
  if direction.value.z != 0:
    raise ValueError("Bad direction for a grid: " + str(direction))
  for i in range(SIZE):
    g = Grid()
    for line in range(SIZE):
      g.fill_line(
          direction,
          line,
          start.get_line(direction, line - i) if line >= i else end.get_line(direction, (line - i) % SIZE))
    yield g
  yield end

def wipe(direction, start, end):
  if direction.value.z != 0:
    raise ValueError("Bad direction for a grid: " + str(direction))
  for i in range(SIZE):
    g = Grid()
    for line in range(SIZE):
      g.fill_line(
          direction,
          line,
          start.get_line(direction, line) if line >= i else end.get_line(direction, line))
    yield g
  yield end

def random_transition(start, end):
  return random.choice([
    functools.partial(scroll, Direction.UP),
    functools.partial(wipe, Direction.RIGHT),
  ])(start, end)

from cube import *
from display import *
import random
import generators
import functools

# Each transition is a generator that returns all of the frames in the
# transition, including the start and end frames passed to it.

def scroll(direction, start, end):
  for i in range(SIZE):
    c = Cube()
    for layer in range(SIZE):
      c.fill_layer(
          direction,
          layer,
          start.get_layer(direction, layer - i) if layer >= i else end.get_layer(direction, (layer - i) % SIZE))
    yield c
  yield end

def wipe(direction, start, end):
  for i in range(SIZE):
    c = Cube()
    for layer in range(SIZE):
      c.fill_layer(
          direction,
          layer,
          start.get_layer(direction, layer) if layer >= i else end.get_layer(direction, layer))
    yield c
  yield end

def random_transition(start, end):
  return random.choice([
    functools.partial(scroll, Direction.UP),
    functools.partial(wipe, Direction.RIGHT),
  ])(start, end)

def random_scroll_transition(start, end):
  return random.choice([
    functools.partial(scroll, d) for d in Direction
  ])(start, end)

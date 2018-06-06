from .cube import *
from display import *

def autoscroll(layer_generator, direction = Direction.BACK):
  c = Cube()
  while True:
    for val in layer_generator:
      if type(val) is bool:
        # A boolean means clear the cube and finish before continuing.
        for i in range(c.size):
          scroll_back(c, direction)
          yield c.copy()
          yield True
        continue
      scroll_back(c, direction, new_layer = val)
      yield c.copy()

def scroll_back(cube, direction, new_layer = Colour.BLACK):
  for i in range(cube.size - 1):
    cube.fill_layer(direction, i, cube.get_layer(direction, i + 1))
  cube.fill_layer(direction, cube.size - 1, new_layer)


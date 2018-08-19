from .interactive import *
from visuals.cube import *
from display import *
import random

def parse_input(input):
  values = input.split(',')
  if len(values) != SIZE:
    return None
  return [int(values[i]) for i in range(len(values))]

def create_layer(input):
  if input is None:
    return None
  return [[hue_to_colour(x * 360 / 7) if y >= (8 - input[x]) else Colour.BLACK for y in range(SIZE)] for x in range(SIZE)]

class Spectrogram(Interactive):

  def run(self):
    self.clear_input()
    c = Cube()
    while True:
      yield wait_for_input(value = c.copy())
      input = self.get_input()
      if input is not None:
        grid = create_layer(parse_input(input))
        if grid is not None:
          scroll_back(c, Direction.BACK, new_layer = grid)

def scroll_back(cube, direction, new_layer = Colour.BLACK):
  for i in range(cube.size - 1):
    cube.fill_layer(direction, i, cube.get_layer(direction, i + 1))
  cube.fill_layer(opposite_direction(direction), 0, new_layer)

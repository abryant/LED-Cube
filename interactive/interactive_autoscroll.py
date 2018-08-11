from .interactive import *
from visuals.cube import *
from display import *
import random

def parse_colour(input):
  parts = input.split(',')
  if len(parts) != 3:
    return None
  return Colour((int(parts[0]), int(parts[1]), int(parts[2])))

def parse_input(input):
  lines = input.split('|')
  if len(lines) != SIZE:
    return None
  grid = [[Colour.BLACK for i in range(SIZE)] for j in range(SIZE)]
  for x, line in enumerate(lines):
    pixels = line.split(';')
    if len(pixels) != SIZE:
      return None
    for y, pixel in enumerate(pixels):
      colour = parse_colour(pixel)
      if colour is None:
        return None
      grid[x][y] = colour
  return grid

class Autoscroll(Interactive):

  def run(self):
    self.clear_input()
    c = Cube()
    while True:
      yield wait_for_input(value = c.copy())
      input = self.get_input()
      if input is not None:
        grid = parse_input(input)
        if grid is not None:
          scroll_back(c, Direction.BACK, new_layer = grid)

def scroll_back(cube, direction, new_layer = Colour.BLACK):
  for i in range(cube.size - 1):
    cube.fill_layer(direction, i, cube.get_layer(direction, i + 1))
  cube.fill_layer(opposite_direction(direction), 0, new_layer)

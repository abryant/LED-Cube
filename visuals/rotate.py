from .cube import *
from display import *
from . import rainbow
import generators

def rotate(up_direction, steps, cube):
  """Rotates a cube around the given up_direction, by the given number of 90 degree steps"""
  c = Cube(cube.size)
  for layer in range(cube.size):
    grid = cube.get_layer(up_direction, layer)
    for i in range(steps):
      grid = [[grid[y][cube.size - 1 - x] for y in range(cube.size)] for x in range(cube.size)]
    c.fill_layer(up_direction, layer, grid)
  return c


def rotate_cube(cube, up_direction):
  """Generator function that rotates the cube clockwise around the given up_direction"""
  while True:
    for i in range(SIZE * 4 - 4):
      c = cube.copy()
      for layer in range(SIZE // 2):
        # layer 0 is outermost
        layer_size = SIZE * 4 - 4 - 8 * layer
        layer_pos = i * layer_size // (SIZE * 4 - 4)
        rotate_layer(c, up_direction, layer, layer_pos)
      yield c
    yield True


def rotate_layer(cube, up_direction, layer, steps):
  """Rotates the given rotational-layer (0 being outermost) of the cube by the given number of steps clockwise around up_direction"""
  low = layer
  high = SIZE - 1 - layer
  length = SIZE - (2 * layer)
  pos = ([(low + i, low) for i in range(length - 1)]
       + [(high, low + i) for i in range(length - 1)]
       + [(high - i, high) for i in range(length - 1)]
       + [(low, high - i) for i in range(length - 1)])
  lines = [cube.get_line(up_direction, convert_face_coordinates(up_direction, p, 0)) for p in pos]
  for i in range(len(pos)):
    cube.fill_line(up_direction, convert_face_coordinates(up_direction, pos[(i + steps) % len(pos)], 0), lines[i])

def make_rotated_hue_cube():
  cube = Cube()
  for i in range(SIZE * 4 - 4):
    hue = 360 * i / (SIZE * 4 - 4)
    cube.fill_line(Direction.UP, convert_face_coordinates(Direction.UP, (0, 0), 0), hue_to_colour(hue))
    rotate_layer(cube, Direction.UP, 0, 1)
  return cube


if __name__ == "__main__":
  cube = rainbow.make_colour_cube()
  with Display() as d:
    generators.generate(d, generators.sequence([
      generators.repeat(rotate_cube(cube, Direction.UP), 5),
      generators.repeat(rotate_cube(cube, Direction.LEFT), 5),
      generators.repeat(rotate_cube(cube, Direction.FRONT), 5),
    ]))



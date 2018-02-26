from config import SIZE
from cube import *
from display import *
import generators
import random

t_shape = [Pos(0, 0, 0), Pos(1, 0, 0), Pos(2, 0, 0),
                         Pos(1, 1, 0)]

s_shape =               [Pos(1, 0, 0), Pos(2, 0, 0),
           Pos(0, 1, 0), Pos(1, 1, 0)]

z_shape = [Pos(0, 0, 0), Pos(1, 0, 0),
                         Pos(1, 1, 0), Pos(2, 1, 0)]

i_shape = [Pos(0, 0, 0), Pos(1, 0, 0), Pos(2, 0, 0), Pos(3, 0, 0)]

o_shape = [Pos(0, 0, 0), Pos(1, 0, 0),
           Pos(0, 1, 0), Pos(1, 1, 0)]

l_shape = [Pos(0, 0, 0), Pos(1, 0, 0), Pos(2, 0, 0),
           Pos(0, 1, 0)]

j_shape = [Pos(0, 0, 0),
           Pos(0, 1, 0), Pos(1, 1, 0), Pos(2, 1, 0)]

# Each shape gets a consistent colour.
all_shapes = [z_shape, s_shape, j_shape, i_shape, t_shape, o_shape, l_shape]
shape_colours = [Colour.RED, Colour.GREEN, Colour.BLUE, Colour.CYAN, Colour.MAGENTA, Colour.YELLOW, Colour.WHITE]

def rotate_shape(shape):
  for xrot in range(random.randint(0, 3)):
    # rotate 90 degrees on x axis
    shape = [Pos(p.x, p.z, -p.y) for p in shape]
  for yrot in range(random.randint(0, 3)):
    # rotate 90 degrees on y axis
    shape = [Pos(p.z, p.y, -p.x) for p in shape]
  return shape

def position_in_xz_bounds(shape):
  min_x = min([p.x for p in shape])
  max_x = max([p.x for p in shape])
  min_z = min([p.z for p in shape])
  max_z = max([p.z for p in shape])
  shift_x = -min_x + random.randint(0, SIZE - (max_x + 1 - min_x))
  shift_z = -min_z + random.randint(0, SIZE - (max_z + 1 - min_z))
  # position above the y axis, so the lowest point is at -1 (positive y means further down)
  max_y = max([p.y for p in shape])
  shift_y = -max_y - 1
  return [Pos(p.x + shift_x, p.y + shift_y, p.z + shift_z) for p in shape]

def can_fall(shape, cube):
  new_shape = [Pos(p.x, p.y + 1, p.z) for p in shape]
  for p in new_shape:
    if p.y >= SIZE or (p.is_in_bounds() and cube.get(p) != Colour.BLACK):
      return False
  return True

def combine(cube, shape, colour):
  c = cube.copy()
  for p in shape:
    if p.is_in_bounds():
      c.set(p, colour)
  return c

def tetris():
  while True:
    c = Cube()
    while True:
      i = random.randint(0, len(all_shapes) - 1)
      s = position_in_xz_bounds(rotate_shape(all_shapes[i]))
      colour = shape_colours[i]
      yield c
      yield c
      if not can_fall(s, c):
        break
      while can_fall(s, c):
        s = [Pos(p.x, p.y + 1, p.z) for p in s]
        yield combine(c, s, colour)
      if not all([p.is_in_bounds() for p in s]):
        break
      c = combine(c, s, colour)
    yield True

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, tetris(), delay = 0.25)


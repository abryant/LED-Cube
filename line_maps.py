# Mappings from line to cube.
from config import SIZE
from cube import *
from display import *
import line
import rotate
import generators
import functools

def control_order(colours):
  assert len(colours) == (SIZE * SIZE * SIZE)
  result = Cube()
  for layer_index in range(SIZE):
    layer = colours[(layer_index * SIZE * SIZE):((layer_index + 1) * SIZE * SIZE)]
    if (layer_index % 2) == 0:
      layer.reverse()
    for line_index in range(SIZE):
      line = layer[(line_index * SIZE):((line_index + 1) * SIZE)]
      if (line_index % 2) == 0:
        line.reverse()
      result.grid[layer_index][line_index] = line
  return result

def spiral(colours):
  assert len(colours) == (SIZE * SIZE * SIZE)
  cube = Cube()
  for layer in range((SIZE + 1) // 2):
    low = layer
    high = SIZE - 1 - layer
    length = high - low
    for slice_index in range(SIZE):
      pos = ([(low + i, low) for i in range(length)]
           + [(high, low + i) for i in range(length)]
           + [(high - i, high) for i in range(length)]
           + [(low, high - i) for i in range(length)])
      if length == 0:
        pos = [(low, low)]
      real_slice_index = slice_index if (layer % 2) == 0 else SIZE - 1 - slice_index
      for i in range(len(pos)):
        cube.set(convert_face_coordinates(Direction.FRONT, pos[i], real_slice_index), colours[i])
      colours = colours[len(pos):]
  return cube

def line_to_cube(line_generator, cube_transform = control_order):
  for val in line_generator:
    if type(val) is bool:
      yield val
    else:
      yield cube_transform(val)


if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, generators.transform(line_to_cube(generators.sequence([
        line.scroll_in(line.rainbow()),
        generators.repeat(line.cycle(line.rainbow(), dir=6), 2),
        line.scroll_out(line.rainbow()),
      ]), spiral), functools.partial(rotate.rotate, Direction.LEFT, 1)))



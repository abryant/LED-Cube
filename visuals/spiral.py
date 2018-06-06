from .autoscroll import *
from display import *
from itertools import chain
import random

def find_line_points(start_dir, move_dir):
  if not start_dir.value.is_2d() or not move_dir.value.is_2d():
    raise "Used a 3D direction in find_line_points()"
  half_size = (SIZE + 1) // 2
  if start_dir.value.x == 0:
    x = SIZE // 2
    if SIZE % 2 == 0 and move_dir.value.x < 0:
      x -= 1
    base_y = SIZE // 2
    if SIZE % 2 == 0 and start_dir.value.y < 0:
      base_y -= 1
    return [(x, base_y + (y if start_dir.value.y > 0 else -y)) for y in range(half_size)]
  else:
    y = SIZE // 2
    if SIZE % 2 == 0 and move_dir.value.y < 0:
      y -= 1
    base_x = SIZE // 2
    if SIZE % 2 == 0 and start_dir.value.x < 0:
      base_x -= 1
    return [(base_x + (x if start_dir.value.x > 0 else -x), y) for x in range(half_size)]

def corner_2d(start_dir, move_dir):
  points = find_line_points(start_dir, move_dir)
  half_size = (SIZE + 1) // 2
  move_x = move_dir.value.x
  move_y = move_dir.value.y
  for i in range(half_size):
    ratio = i / (half_size - 1)
    yield [(points[j][0] + move_x * round(ratio * j), points[j][1] + move_y * round(ratio * j)) for j in range(len(points))]
  points = find_line_points(move_dir, start_dir)
  move_x = start_dir.value.x
  move_y = start_dir.value.y
  for i in range(half_size - 2, -1 if SIZE % 2 == 0 else 0, -1):
    ratio = i / (half_size - 1)
    yield [(points[j][0] + move_x * round(ratio * j), points[j][1] + move_y * round(ratio * j)) for j in range(len(points))]

def combine_frames(list1, list2):
  result = []
  for i in range(max(len(list1), len(list2))):
    result.append(list1[i] + list2[i])
  return result

def spiral_2d():
  hue = 0
  h = 10
  frames = (combine_frames(list(corner_2d(Direction.UP, Direction.RIGHT)),
                           list(corner_2d(Direction.DOWN, Direction.LEFT))) +
            combine_frames(list(corner_2d(Direction.RIGHT, Direction.DOWN)),
                           list(corner_2d(Direction.LEFT, Direction.UP))))
  while True:
    for frame in frames:
      yield [[hue_to_colour(hue) if (x, y) in frame else Colour.BLACK for y in range(SIZE)] for x in range(SIZE)]
      hue = (hue + h) % 360

def spiral():
  return autoscroll(spiral_2d(), direction = Direction.BACK)

def main():
  with Display() as d:
    generators.generate(d, spiral(), delay = 0.05)

if __name__ == '__main__':
  main()

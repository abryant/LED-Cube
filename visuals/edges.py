import generators
from display import *
from .cube import *
import random

def pick_random_edge():
  dir_a = random.choice([d for d in Direction])
  dir_b = random.choice([d for d in Direction if not is_same_axis(dir_a, d)])
  return (dir_a, dir_b)

def get_opposite_edge(edge):
  dir_a, dir_b = edge
  return opposite_direction(dir_a), opposite_direction(dir_b)

def adjacent_edges(edge):
  dir_a, dir_b = edge
  other_dirs = [d for d in Direction if not (is_same_axis(dir_a, d) or is_same_axis(dir_b, d))]
  return [(dir_a, other_dirs[0]), (dir_a, other_dirs[1]), (dir_b, other_dirs[0]), (dir_b, other_dirs[1])]

def get_common_direction(edge_a, edge_b):
  return [d for d in edge_a if d in edge_b][0]

def find_edge_points(dir_a, dir_b, line_dir):
  a_component = dir_a.value * (SIZE - 1) if is_direction_positive(dir_a) else Pos(0, 0, 0)
  b_component = dir_b.value * (SIZE - 1) if is_direction_positive(dir_b) else Pos(0, 0, 0)
  line_component = line_dir.value if is_direction_positive(line_dir) else opposite_direction(line_dir).value
  points = [a_component + b_component + (line_component * i) for i in range(SIZE)]
  if is_direction_positive(line_dir):
    points.reverse()
  return points

def generate_corner(edge, new_edge, hue1, hue2):
  move_face = get_common_direction(edge, new_edge)
  first_dir = [d for d in edge if d != move_face][0]
  opposite_first_dir = opposite_direction(first_dir)
  second_dir = [d for d in new_edge if d != move_face][0]
  opposite_second_dir = opposite_direction(second_dir)
  points = find_edge_points(move_face, first_dir, second_dir)
  if abs(hue2 - hue1) > abs(hue2 + 360 - hue1):
    hue2 += 360
  animation_gaps = (SIZE - 1) * 2
  h = (hue2 - hue1) / animation_gaps
  current_hue = hue1
  for i in range(SIZE):
    c = Cube()
    ratio = i / (c.size - 1)
    for j in range(len(points)):
      c.set(points[j] + (opposite_first_dir.value * round(ratio * j)), hue_to_colour(current_hue))
    yield c
    current_hue += h
  points = find_edge_points(move_face, second_dir, first_dir)
  for i in range(SIZE - 2, -1, -1):
    c = Cube()
    ratio = i / (c.size - 1)
    for j in range(len(points)):
      c.set(points[j] + (opposite_second_dir.value * round(ratio * j)), hue_to_colour(current_hue))
    yield c
    current_hue += h


def generate_opposite_corners(edge, new_edge, hue, new_hue):
  gen_a = generate_corner(edge, new_edge, hue, new_hue)
  gen_b = generate_corner(
      get_opposite_edge(edge), get_opposite_edge(new_edge),
      get_opposite_hue(hue), get_opposite_hue(new_hue))
  for val_a in gen_a:
    val_b = next(gen_b)
    yield combine_cubes(val_a, val_b)

hues = [Colour.RED_HUE, Colour.GREEN_HUE, Colour.BLUE_HUE]

def edges():
  hue = random.choice(hues)
  previous_edge = None
  edge = pick_random_edge()
  while True:
    new_edge = random.choice([e for e in adjacent_edges(edge) if e != previous_edge])
    new_hue = random.choice([h for h in hues if h != hue])
    for val in generate_opposite_corners(edge, new_edge, hue, new_hue):
      yield val
    previous_edge = edge
    edge = new_edge
    hue = new_hue
    yield True

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, edges(), delay=0.05)


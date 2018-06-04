import generators
from display import *
from .cube import *
import random

def get_layer_coord(direction, index):
  """Gets the 0,0 coordinate on the given layer, where layer 0 is the one furthest in the given direction."""
  return (direction.value * (SIZE - 1 - index)) if is_direction_positive(direction) else (-direction.value * index)

def find_face_points(face_dir, line_dir):
  face_component = face_dir.value * (SIZE - 1) if is_direction_positive(face_dir) else Pos(0, 0, 0)
  line_component = line_dir.value if is_direction_positive(line_dir) else opposite_direction(line_dir).value
  perpendicular_dir = perpendicular_direction(face_dir, line_dir)
  points = [[face_component + (perpendicular_dir.value * j) + (line_component * i) for j in range(SIZE)] for i in range(SIZE)]
  if is_direction_positive(line_dir):
    points.reverse()
  return points

def generate_corner(start_dir, end_dir, hue1, hue2):
  opposite_start_dir = opposite_direction(start_dir)
  opposite_end_dir = opposite_direction(end_dir)
  points = find_face_points(start_dir, end_dir)
  if abs(hue2 - hue1) > abs(hue2 + 360 - hue1):
    hue2 += 360
  animation_gaps = (SIZE - 1) * 2
  h = (hue2 - hue1) / animation_gaps
  current_hue = hue1
  for i in range(SIZE):
    c = Cube()
    ratio = i / (c.size - 1)
    for j in range(len(points)):
      for k in range(len(points[j])):
        c.set(points[j][k] + (opposite_start_dir.value * round(ratio * j)), hue_to_colour(current_hue))
    yield c
    current_hue += h
  points = find_face_points(end_dir, start_dir)
  for i in range(SIZE - 2, -1, -1):
    c = Cube()
    ratio = i / (c.size - 1)
    for j in range(len(points)):
      for k in range(len(points[j])):
        c.set(points[j][k] + (opposite_end_dir.value * round(ratio * j)), hue_to_colour(current_hue))
    yield c
    current_hue += h

def straight(end_direction, hue1, hue2):
  if abs(hue2 - hue1) > abs(hue2 + 360 - hue1):
    hue2 += 360
  h = (hue2 - hue1) / (SIZE - 1)
  while True:
    for i in range(SIZE):
      c = Cube()
      c.fill_layer(end_direction, SIZE - 1 - i, hue_to_colour(hue1 + (h * i)))
      yield c
    yield True

hues = [Colour.RED_HUE, Colour.GREEN_HUE, Colour.BLUE_HUE]


def faces():
  hue = random.choice(hues)
  direction = random.choice([d for d in Direction])
  while True:
    new_direction = random.choice([d for d in Direction if d != direction])
    new_hue = random.choice([h for h in hues if h != hue])
    if new_direction.value == -direction.value:
      gen = straight(new_direction, hue, new_hue)
    else:
      gen = generate_corner(direction, new_direction, hue, new_hue)
    for val in gen:
      if type(val) is bool:
        break
      yield val
    direction = new_direction
    hue = new_hue
    c = Cube()
    c.fill_layer(direction, 0, hue_to_colour(hue))
    yield c
    yield c
    yield c
    yield c
    yield True

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, faces(), delay=0.05)


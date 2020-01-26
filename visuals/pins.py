from .cube import *
from display import *
import random

def fade(hue1, hue2, amount):
  if abs(hue2 - hue1) > abs(hue2 + 360 - hue1):
    hue2 = hue2 + 360
  if abs(hue1 - hue2) > abs(hue1 + 360 - hue2):
    hue1 = hue1 + 360
  return hue_to_colour(int(hue1 + (hue2 - hue1) * amount))

def xz_to_coord(xz):
  x, z = xz
  return Direction.RIGHT.value * x + Direction.FRONT.value * z

def pin(size, hue1, hue2):
  yield [fade(hue1, hue2, 0) if x == 0 else Colour.BLACK for x in range(size)]
  while True:
    for i in range(1, size):
      yield [fade(hue1, hue2, i / (size - 1)) if x == i else Colour.BLACK for x in range(size)]
    yield True
    for i in range(size - 2, -1, -1):
      yield [fade(hue1, hue2, i / (size - 1)) if x == i else Colour.BLACK for x in range(size)]
    yield True

def pins_ordered(hue1, hue2):
  c = Cube()
  pins = [[pin(c.size, hue1, hue2) for x in range(c.size)] for z in range(c.size)]
  for x in range(c.size):
    for z in range(c.size):
      c.fill_line(Direction.DOWN, xz_to_coord((x, z)), next(pins[x][z]))
  yield c.copy()
  while True:
    for x in range(c.size):
      for z in range(c.size):
        for line in pins[x][z]:
          if type(line) is bool:
            break
          c.fill_line(Direction.DOWN, xz_to_coord((x, z)), line)
          yield c.copy()
        yield True

def pins_random(hue1, hue2):
  c = Cube()
  pins = [[pin(c.size, hue1, hue2) for x in range(c.size)] for z in range(c.size)]
  for x in range(c.size):
    for z in range(c.size):
      c.fill_line(Direction.DOWN, xz_to_coord((x, z)), next(pins[x][z]))
  yield c.copy()
  while True:
    x = random.randint(0, c.size - 1)
    z = random.randint(0, c.size - 1)
    for line in pins[x][z]:
      if type(line) is bool:
        break
      c.fill_line(Direction.DOWN, xz_to_coord((x, z)), line)
      yield c.copy()
    yield True

def pins():
  c = Cube()
  current_hue = random.choice(Colour.ALL_HUES)
  c.fill_layer(Direction.UP, 0, hue_to_colour(current_hue))
  up = False
  while True:
    next_hue = random.choice([h for h in Colour.ALL_HUES if h != current_hue])
    all_coords = [(x, z) for x in range(c.size) for z in range(c.size)]
    random.shuffle(all_coords)
    for i in range(len(all_coords) + c.size):
      for j in range(max(0, i - (c.size - 1)), min(i, len(all_coords))):
        x, z = all_coords[j]
        y = i - j # 7-1
        prevy = i - j - 1 # 6-0
        colour = fade(current_hue, next_hue, y / (c.size - 1))
        if up:
          y = c.size - 1 - y # 0-6
          prevy = c.size - 1 - prevy # 1-7
        c.set(xz_to_coord((x, z)) + Direction.DOWN.value * prevy, Colour.BLACK)
        c.set(xz_to_coord((x, z)) + Direction.DOWN.value * y, colour)
      yield c.copy()
    current_hue = next_hue
    up = not up
    yield True

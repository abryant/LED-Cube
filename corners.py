from cube import *
from display import *
import generators
import random

def draw_outline(p1, p2, colour):
  minp = Pos(min(p1.x, p2.x), min(p1.y, p2.y), min(p1.z, p2.z))
  maxp = Pos(max(p1.x, p2.x), max(p1.y, p2.y), max(p1.z, p2.z))
  c = Cube()
  for x in range(minp.x, maxp.x + 1):
    c.set(Pos(x, minp.y, minp.z), colour)
    c.set(Pos(x, minp.y, maxp.z), colour)
    c.set(Pos(x, maxp.y, minp.z), colour)
    c.set(Pos(x, maxp.y, maxp.z), colour)
  for y in range(minp.y, maxp.y + 1):
    c.set(Pos(minp.x, y, minp.z), colour)
    c.set(Pos(minp.x, y, maxp.z), colour)
    c.set(Pos(maxp.x, y, minp.z), colour)
    c.set(Pos(maxp.x, y, maxp.z), colour)
  for z in range(minp.z, maxp.z + 1):
    c.set(Pos(minp.x, minp.y, z), colour)
    c.set(Pos(minp.x, maxp.y, z), colour)
    c.set(Pos(maxp.x, minp.y, z), colour)
    c.set(Pos(maxp.x, maxp.y, z), colour)
  return c

hues = [Colour.RED_HUE, Colour.YELLOW_HUE, Colour.GREEN_HUE, Colour.CYAN_HUE, Colour.BLUE_HUE, Colour.MAGENTA_HUE]

def shrink_and_grow(hue1, hue2):
  if abs(hue2 - hue1) > abs(hue2 + 360 - hue1):
    hue2 += 360
  h = (hue2 - hue1) / 6 # 7 animation frames (the last of which is skipped), so 6 gaps
  currenthue = hue1
  for i in range(SIZE - 1, 0, -1):
    yield draw_outline(Pos(0, 0, 0), Pos(i, i, i), hue_to_colour(currenthue))
    currenthue += h
  for i in range(0, SIZE - 1):
    yield draw_outline(Pos(0, 0, 0), Pos(i, i, i), hue_to_colour(currenthue))
    currenthue += h

def flip(gen, flip_x, flip_y, flip_z):
  for c in gen:
    flipped = Cube(size = c.size)
    for x in range(c.size):
      for y in range(c.size):
        for z in range(c.size):
          destpos = Pos(
              (SIZE - 1 - x) if flip_x else x,
              (SIZE - 1 - y) if flip_y else y,
              (SIZE - 1 - z) if flip_z else z)
          flipped.set(destpos, c.get(Pos(x, y, z)))
    yield flipped

def corners():
  hue = random.choice(hues)
  corner = -1
  while True:
    newcorner = random.choice([i for i in [0, 1, 2, 3, 4, 5, 6, 7] if i != corner])
    newhue = random.choice([h for h in hues if h != hue])
    for c in flip(shrink_and_grow(hue, newhue), (newcorner & 4) == 4, (newcorner & 2) == 2, (newcorner & 1) == 1):
      yield c
    yield draw_outline(Pos(0, 0, 0), Pos(SIZE - 1, SIZE - 1, SIZE - 1), hue_to_colour(newhue))
    hue = newhue
    corner = newcorner
    yield True

def main():
  with Display() as d:
    generators.generate(d, corners(), delay = 0.1)

if __name__ == '__main__':
  main()

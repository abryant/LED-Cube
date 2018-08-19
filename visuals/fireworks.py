from .cube import *
from display import *
import generators
import random
import math

def generate_movement_list(pos_a, pos_b):
  if pos_a == pos_b:
    return [pos_a]
  x1, y1, z1 = pos_a.x, pos_a.y, pos_a.z
  x2, y2, z2 = pos_b.x, pos_b.y, pos_b.z
  length = max([abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)]) * 2
  vx, vy, vz = (x2 - x1) / length, (y2 - y1) / length, (z2 - z1) / length
  return [Pos(x1 + round(vx*i), y1 + round(vy*i), z1 + round(vz*i)) for i in range(length+1)]

def firework():
  height = random.randint(SIZE / 2, SIZE - 2)
  x = random.randint(1, SIZE - 2)
  z = random.randint(1, SIZE - 2)
  colour = hue_to_colour(random.choice(Colour.ALL_HUES))
  for i in range(height + 1):
    c = Cube()
    c.set(Pos(x, SIZE - 1 - i, z), colour)
    yield c.copy()
    yield c
  final_positions = []
  sphere_size = SIZE/2
  for lx in range(SIZE):
    for lz in range(SIZE):
      lxd = lx - x
      lzd = lz - z
      if (lxd**2 + lzd**2) < sphere_size**2:
        hd = math.sqrt(sphere_size**2 - (lxd**2 + lzd**2))
        h = height + random.randint(round(-hd), round(hd))
        h = max(0, min(SIZE - 1, h))
        final_positions.append(Pos(lx, SIZE - 1 - h, lz))
  movement_lists = []
  for i in range(len(final_positions)):
    movement_lists.append(generate_movement_list(Pos(x, SIZE - 1 - height, z), final_positions[i]))
  maxlen = max([len(movement_lists[i]) for i in range(len(movement_lists))])
  for i in range(maxlen):
    c = Cube()
    for j in range(len(movement_lists)):
      if i < len(movement_lists[j]):
        c.set(movement_lists[j][i], colour)
      else:
        c.set(movement_lists[j][-1], colour)
    yield c.copy()
    if i == maxlen - 1:
      yield c

def fireworks():
  while True:
    yield from firework()
    yield True

def main():
  with Display() as d:
    generators.generate(d, fireworks(), delay = 0.1)

if __name__ == '__main__':
  main()

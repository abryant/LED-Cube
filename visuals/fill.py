from .cube import *
import random

def fill():
  c = Cube()
  colour = Colour.cyan()
  on = True
  while True:
    all_coords = [(x, y, z) for x in range(c.size) for y in range(c.size) for z in range(c.size)]
    random.shuffle(all_coords)
    for coord in all_coords:
        if on:
          c.set(Pos(*coord), colour)
        else:
          c.set(Pos(*coord), Colour.BLACK)
        yield c.copy()
    on = not on
    yield True
from .cube import *
import random

def fill():
  c = Cube()
  on = True
  while True:
    colour = hue_to_colour(random.randint(0, 359))
    all_coords = [(x, y, z) for x in range(c.size) for y in range(c.size) for z in range(c.size)]
    random.shuffle(all_coords)
    for counter, coord in enumerate(all_coords):
        if on:
          c.set(Pos(*coord), colour)
        else:
          c.set(Pos(*coord), Colour.BLACK)
        if counter % c.size == 7:
          yield c.copy()
    on = not on
    yield True
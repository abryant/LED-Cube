from .cube import *
import random

def fill():
  c = Cube()
  on = True
  while True:
    colour = hue_to_colour(random.randint(0, 359))
    all_positions = [Pos(x, y, z) for x in range(c.size) for y in range(c.size) for z in range(c.size)]
    random.shuffle(all_positions)
    for counter, position in enumerate(all_positions):
        if on:
          c.set(position, colour)
        else:
          c.set(position, Colour.BLACK)
        if counter % c.size == c.size - 1:
          yield c.copy()
    on = not on
    yield True
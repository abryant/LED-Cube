from .cube import *
from display import *
import generators
import random

def layers():
  hue = 0
  h = 30
  half_size = (SIZE + 1) // 2
  colours = [Colour.BLACK for i in range(half_size)]
  while True:
    c = Cube()
    for i in range(half_size):
      c.fill(Pos(i, i, i), Pos(SIZE - 1 - i, SIZE - 1 - i, SIZE - 1 - i), colours[i])
    yield c
    colours = colours[1:] + [hue_to_colour(hue)]
    hue = (hue + h) % 360

def main():
  with Display() as d:
    generators.generate(d, layers(), delay = 0.1)

if __name__ == '__main__':
  main()

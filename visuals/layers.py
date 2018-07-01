from .cube import *
from display import *
import generators
import random

def layers():
  half_size = (SIZE + 1) // 2
  possible_colours = [Colour.red(), Colour.green(), Colour.blue()]
  colours = [Colour.BLACK for i in range(half_size - 1)] + [possible_colours[0]]
  possible_colours = possible_colours[1:] + [possible_colours[0]]
  index = 0
  while True:
    c = Cube()
    for i in range(half_size):
      c.fill(Pos(i, i, i), Pos(SIZE - 1 - i, SIZE - 1 - i, SIZE - 1 - i), colours[i])
    yield c
    new_colour = Colour.BLACK
    index += 1
    if index % 2 == 0:
      new_colour = possible_colours[0]
      possible_colours = possible_colours[1:] + [new_colour]
    colours = colours[1:] + [new_colour]

def main():
  with Display() as d:
    generators.generate(d, layers(), delay = 0.1)

if __name__ == '__main__':
  main()

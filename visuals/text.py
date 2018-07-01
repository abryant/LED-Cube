from display import *
from .autoscroll import *
from .grid import *
from .position import *
from font.font import draw_character
import generators
import functools
from . import grid_transitions

def display_character(c, colour, times = 10):
  while True:
    for i in range(times):
      yield Grid.from_array(draw_character(c, colour, Colour.BLACK))
    yield True

def marquee(text, colours):
  if type(colours) is not list:
    colours = [colours]
  text_characters = [display_character(text[i], colours[i % len(colours)]) for i in range(len(text))]
  return generators.sequence(
      [display_character(" ", Colour.BLACK)] + text_characters + [display_character(" ", Colour.BLACK)],
      transition = functools.partial(grid_transitions.scroll, Direction.RIGHT))

def text_2d(text, colours):
  if type(colours) is not list:
    colours = [colours]
  while True:
    for i in range(len(text)):
      yield draw_character(text[i], colours[i % len(colours)], Colour.BLACK)
      yield True

def text(text, colours):
  return generators.repeat(autoscroll(text_2d(text, colours), direction = Direction.FRONT), len(text))

def main():
  with Display() as d:
    generators.generate(d, marquee("ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789", [Colour.red(), Colour.green(), Colour.blue()]))

if __name__ == "__main__":
  main()

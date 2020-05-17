from display import *
from .autoscroll import *
from .grid import *
from .position import *
from font.font import draw_character
import generators
import functools
import operator
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

def marquee_front_right(text, colours):
  if type(colours) is not list:
    colours = [colours]
  text = '  ' + text + '  '
  letters = [draw_character(text[i], colours[i % len(colours)], Colour.BLACK) for i in range(len(text))]
  long_grid = functools.reduce(operator.iconcat, letters, [])
  c = Cube()
  display_size = c.size * 2 - 1
  while True:
    for start in range(len(long_grid) - display_size + 1):
      short_grid = long_grid[start:start+display_size]
      # front face
      for i in range(c.size):
        c.fill_line(Direction.DOWN, convert_face_coordinates(Direction.FRONT, (i, 0), 0), short_grid[i])
      # right face
      for i in range(c.size - 1):
        c.fill_line(Direction.DOWN, convert_face_coordinates(Direction.RIGHT, (i + 1, 0), 0), short_grid[c.size + i])
      yield c.copy()
    yield True


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

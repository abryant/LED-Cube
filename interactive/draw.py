from .interactive import *
from visuals.cube import *
from display import *
import random

def parse_input(input):
  parts = input.split(';')
  if len(parts) != 2 or not parts[0].startswith('p=') or not parts[1].startswith('c='):
    return None, None
  pos_parts = parts[0][2:].split(',')
  colour_parts = parts[1][2:].split(',')
  if len(pos_parts) != 3 or len(colour_parts) != 3:
    return None, None
  pos = Pos(int(pos_parts[0]), int(pos_parts[1]), int(pos_parts[2]))
  colour = Colour((int(colour_parts[0]), int(colour_parts[1]), int(colour_parts[2])))
  return pos, colour

class Draw(Interactive):

  def run(self):
    self.clear_input()
    c = Cube()
    while True:
      yield wait_for_input(value = c.copy())
      input = self.get_input()
      if input is not None:
        pos, colour = parse_input(input)
        if pos is not None and colour is not None:
          c.set(pos, colour)


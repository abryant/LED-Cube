from cube import *
from config import SIZE
from display import *

def flash():
  while True:
    yield Cube(colour = Colour.WHITE)
    yield Cube(colour = Colour.BLACK)
    yield True

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, flash())


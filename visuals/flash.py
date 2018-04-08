from .cube import *
from display import *

def flash():
  while True:
    yield Cube(colour = Colour.white())
    yield Cube(colour = Colour.black())
    yield True

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, flash())


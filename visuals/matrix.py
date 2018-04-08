import generators
from display import *
from .cube import *
import random

def matrix_line():
  dot = -1
  cs = [Colour.BLACK for i in range(SIZE)]
  while True:
    if dot == -1:
      for i in range(SIZE):
        cs[i] = Colour((cs[i].r * 0.95, cs[i].g * 0.95, cs[i].b * 0.95))
      if random.randint(0, 100) == 0:
        dot = 0
        cs[0] = Colour((10, 64, 10))
    else:
      for i in range(dot):
        cs[i] = Colour((cs[i].r * 0.95, cs[i].g * 0.95, cs[i].b * 0.95))
      if random.randint(0, 20) == 0:
        cs[dot] = Colour((0, 32, 0))
        dot += 1
        if dot == SIZE:
          dot = -1
        else:
          cs[dot] = Colour((10, 64, 10))
    yield cs

def matrix():
  c = Cube()
  gens = [[matrix_line() for z in range(SIZE)] for x in range(SIZE)]
  while True:
    for x in range(SIZE):
      for z in range(SIZE):
        c.fill_line(Direction.DOWN, Pos(x, 0, z), next(gens[x][z]))
    yield c

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, matrix())


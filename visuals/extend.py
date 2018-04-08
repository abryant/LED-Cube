from .cube import *
from display import *
import generators
import random

def choose_dirs():
  dirs = [
      random.choice([Direction.UP, Direction.DOWN]),
      random.choice([Direction.LEFT, Direction.RIGHT]),
      random.choice([Direction.FRONT, Direction.BACK]),
  ]
  random.shuffle(dirs)
  return dirs

def get_opposite_dirs(dirs):
  return [opposite_direction(d) for d in dirs][::-1]

def compress(cube, dirs):
  c = cube.copy()
  yield c.copy()
  for i in range(len(dirs)):
    for j in range(SIZE - 1, 0, -1):
      c.fill_layer(dirs[i], j, Colour.BLACK)
      yield c.copy()

def extend():
  yield Cube()
  while True:
    cube = Cube(colour = hue_to_colour(random.choice(Colour.ALL_HUES)))
    for c in generators.reverse(compress(cube, choose_dirs())):
      yield c
    for c in compress(cube, choose_dirs()):
      yield c
    yield Cube()
    yield True


def main():
  with Display() as d:
    generators.generate(d, generators.slow(extend()))

if __name__ == '__main__':
  main()

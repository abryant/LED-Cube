from cube import *
from display import *
import generators
import random

def init_cube():
  c = Cube()
  c.fill_layer(Direction.UP, 0, Colour.RED)
  c.fill_layer(Direction.UP, 1, Colour.GREEN)
  c.fill_layer(Direction.UP, 2, Colour.BLUE)
  c.fill_layer(Direction.UP, 3, Colour.WHITE)
  return c

def randomize_cube():
  c = init_cube()
  for i in range(20):
    c = shuffle_step(c)
  return c

def shuffle_step(cube):
  d = random.choice([Direction.UP, Direction.RIGHT, Direction.FRONT])
  layer_num = random.randint(0, 3)
  layer = cube.get_layer(d, layer_num)
  adjust = random.choice([1, -1])
  if random.randint(0, 1) == 0:
    layer = [[layer[(i+adjust) % SIZE][j] for j in range(SIZE)] for i in range(SIZE)]
  else:
    layer = [[layer[i][(j+adjust) % SIZE] for j in range(SIZE)] for i in range(SIZE)]
  new_cube = cube.copy()
  new_cube.fill_layer(d, layer_num, layer)
  return new_cube

def shuffle():
  c = randomize_cube()
  i = 0
  while True:
    c = shuffle_step(c)
    yield c
    if i == 50:
      i = 0
      yield True

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, shuffle())


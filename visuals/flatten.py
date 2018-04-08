from .cube import *
from display import *
import generators
from . import transitions
import random

def random_cube():
  c = Cube()
  for i in range(20):
    p = Pos(random.randint(0, SIZE - 1), random.randint(0, SIZE - 1), random.randint(0, SIZE - 1))
    c.set(p, hue_to_colour(random.choice(Colour.ALL_HUES)))
  return c

def combine_layers(layer1, layer2):
  if layer1 is None:
    return layer2
  return [[layer2[x][y] if layer1[x][y] == Colour.BLACK else layer1[x][y] for y in range(len(layer1[0]))] for x in range(len(layer1))]

def partial_flatten(c, direction, layers):
  final_layer = None
  for i in range(layers):
    layer = c.get_layer(direction, i)
    final_layer = combine_layers(final_layer, layer)
    c.fill_layer(direction, i, Colour.BLACK)
  layer = c.get_layer(direction, layers)
  final_layer = combine_layers(final_layer, layer)
  c.fill_layer(direction, layers, final_layer)
  return c

def flatten_to_side(c, direction):
  for i in range(SIZE):
    yield partial_flatten(c.copy(), direction, i)
  for i in range(SIZE - 1, 0, -1):
    yield partial_flatten(c.copy(), direction, i)
  yield c.copy()

def flatten(iterations = 20):
  c = random_cube()
  i = 0
  last_direction = None
  while True:
    direction = random.choice([d for d in Direction if d != last_direction])
    for c in flatten_to_side(c, direction):
      yield c
    last_direction = direction
    i += 1
    if i == iterations:
      i = 0
      c = random_cube()
      yield True

def main():
  with Display() as d:
    generators.generate(d, generators.sequence([flatten()], transition=transitions.random_scroll_transition))

if __name__ == '__main__':
  main()

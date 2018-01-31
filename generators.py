from time import sleep
from colorsys import hsv_to_rgb
import random

def get_colours(val):
  if callable(getattr(val, 'get_colours', None)):
    return val.get_colours()
  return val

def shuffle(gens):
  while True:
    for val in gens[random.randint(0, len(gens) - 1)]:
      if type(val) is bool:
        break
      yield val
    yield True

def generate(display, gen, delay=0.05):
  while True:
    for colours in gen:
      cs = get_colours(colours)
      if type(cs) is list:
        display.display(cs)
        sleep(delay)

def repeat(gen, times):
  while True:
    for i in range(times):
      for val in gen:
        if type(val) is bool:
          break
        yield val
    yield True

def sequence(gens):
  while True:
    for i in range(len(gens)):
      for val in gens[i]:
        if type(val) is bool:
          break
        yield val
    yield True

def debug(gen):
  for val in gen:
    if type(val) is bool:
      break
    print(val)


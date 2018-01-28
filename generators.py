from time import sleep
from colorsys import hsv_to_rgb
import random

def shuffle(gens):
  while True:
    for val in gens[random.randint(0, len(gens) - 1)]:
      if type(val) is list:
        yield val
      else:
        break
    yield True

def generate(display, gen, delay=0.05):
  while True:
    for colours in gen:
      if type(colours) is list:
        display.display(colours)
        sleep(delay)

def repeat(gen, times):
  while True:
    for i in range(times):
      for val in gen:
        if type(val) is list:
          yield val
        else:
          break
    yield True

def sequence(gens):
  while True:
    for i in range(len(gens)):
      for val in gens[i]:
        if type(val) is list:
          yield val
        else:
          break
    yield True

def debug(gen):
  for val in gen:
    if type(val) is list:
      print(val)
    else:
      break


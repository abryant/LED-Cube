from .autoscroll import *
from display import *
import math
import random

def wave_2d():
  angle = 0
  t = math.pi / SIZE
  hue = 0
  h = 10
  while True:
    yield [[hue_to_colour(hue) if y == round((math.cos(angle) * math.cos(t * x) + 1) * (SIZE - 1) / 2) else Colour.BLACK for y in range(SIZE)] for x in range(SIZE)]
    angle = (angle + t) % (2 * math.pi)
    hue = (hue + h) % 360

def wave():
  return autoscroll(wave_2d(), direction = Direction.RIGHT)

def main():
  with Display() as d:
    generators.generate(d, wave(), delay = 0.05)

if __name__ == '__main__':
  main()

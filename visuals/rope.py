from .autoscroll import *
from display import *
import random

def rope_2d():
  x = SIZE / 2
  y = SIZE / 2
  hue = 0
  h = 10
  while True:
    hue = (hue + h) % 360
    yield [[hue_to_colour(hue) if i == x and j == y else Colour.BLACK for j in range(SIZE)] for i in range(SIZE)]
    if random.randint(0, 1) == 0:
      x = min(SIZE - 1, max(0, x + random.randint(-1, 1)))
      y = min(SIZE - 1, max(0, y + random.randint(-1, 1)))

def rope():
  return autoscroll(rope_2d(), direction = Direction.DOWN)

def main():
  with Display() as d:
    generators.generate(d, rope(), delay = 0.05)

if __name__ == '__main__':
  main()

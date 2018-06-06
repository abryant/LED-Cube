from .autoscroll import *
from display import *
import random

def starfield_2d():
  while True:
    yield [[Colour.white() if random.randint(0, 100) < 5 else Colour.BLACK for j in range(SIZE)] for i in range(SIZE)]

def starfield():
  return autoscroll(starfield_2d(), direction = Direction.FRONT)

def main():
  with Display() as d:
    generators.generate(d, starfield(), delay = 0.05)

if __name__ == '__main__':
  main()

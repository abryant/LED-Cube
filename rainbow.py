from cube import *
from display import *
import generators
from math import atan2, pi
import colorsys

def diagonal_rainbow(scales = Pos(1, 1, 1)):
  c = Cube()
  for x in range(c.size):
    for y in range(c.size):
      for z in range(c.size):
        c.set(Pos(x, y, z), hue_to_colour((x * scales.x + y * scales.y + z * scales.z) * (360 / 6)))
  return c

def make_colour_cube(hue_offset = 0):
  cube = Cube()
  for x in range(SIZE):
    for y in range(SIZE):
      for z in range(SIZE):
        hue = ((atan2(((SIZE - 1) / 2) - z, ((SIZE - 1) / 2) - x) + hue_offset) / 2 / pi) % 1
        sat = 1 - (min([x, z, SIZE - 1 - x, SIZE - 1 - z]) / ((SIZE - 1) // 2))
        val = (20 / 255) * (y + 0.25) / SIZE
        cube.set(Pos(x, y, z), Colour.fromFloats(colorsys.hsv_to_rgb(hue, sat, val)))
  return cube

def rotate_colour_cube(speed):
  while True:
    for i in range(0, 360, 10):
      yield make_colour_cube(hue_offset = i * pi / 180)
    yield True

if __name__ == "__main__":
  with Display('/dev/ttyUSB0') as d:
    generators.generate(d, rotate_colour_cube(pi / 20))

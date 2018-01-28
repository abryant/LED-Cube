from display import *
import generators

def single_frame(colours):
  while True:
    yield colours
    yield True

if __name__ == "__main__":
  with Display('/dev/ttyUSB0') as d:
    generators.generate(d, generators.sequence([
      single_frame([Colour.RED]),
      single_frame([Colour.GREEN]),
      single_frame([Colour.BLUE])
    ]), delay=0.5)

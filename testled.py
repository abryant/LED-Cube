from display import *
import generators

def single_frame(colours):
  while True:
    yield colours
    yield True

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, generators.sequence([
      single_frame([Colour.red()]),
      single_frame([Colour.green()]),
      single_frame([Colour.blue()])
    ]), delay=0.5)

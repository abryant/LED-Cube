from display import *
from cube import *
from sides import sides
from line import scroll_in, scroll_out, cycle, rainbow

if __name__ == "__main__":
  with Display('/dev/ttyUSB0') as d:
    generators.generate(d, generators.sequence([
      generators.sequence([
        scroll_past(Cube(SIZE, Colour((20, 0, 0))), Direction.UP),
        scroll_past(Cube(SIZE, Colour((0, 20, 0))), Direction.RIGHT),
        scroll_past(Cube(SIZE, Colour((0, 0, 20))), Direction.FRONT),
      ]),
      generators.repeat(sides(), 20),
      generators.sequence([
        scroll_in(rainbow()),
        generators.repeat(cycle(rainbow()), 2),
        scroll_out(rainbow()),
      ]),
    ]))


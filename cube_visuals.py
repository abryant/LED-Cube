from display import *
from cube import *
import sides
import line
import rainbow
import transitions
import line_maps

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, generators.sequence([
      generators.sequence([
        scroll_past(Cube(SIZE, Colour((20, 0, 0))), Direction.UP),
        scroll_past(Cube(SIZE, Colour((0, 20, 0))), Direction.RIGHT),
        scroll_past(Cube(SIZE, Colour((0, 0, 20))), Direction.FRONT),
      ]),
      generators.repeat(sides.sides(), 20),
      line_maps.line_to_cube(generators.sequence([
        line.scroll_in(line.rainbow()),
        generators.repeat(line.cycle(line.rainbow()), 2),
        line.scroll_out(line.rainbow()),
      ])),
    ]))


from display import *
from cube import *
import sides
import line
import rainbow
import transitions
import line_maps
import corners
import extend
import flatten
import snakes

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, generators.sequence([
      generators.sequence([
        scroll_past(Cube(SIZE, Colour((BRIGHTNESS, 0, 0))), Direction.UP),
        scroll_past(Cube(SIZE, Colour((0, BRIGHTNESS, 0))), Direction.RIGHT),
        scroll_past(Cube(SIZE, Colour((0, 0, BRIGHTNESS))), Direction.FRONT),
      ]),
      generators.repeat(sides.sides(), 20),
      line_maps.line_to_cube(generators.sequence([
        line.scroll_in(line.rainbow()),
        generators.repeat(line.cycle(line.rainbow()), 2),
        line.scroll_out(line.rainbow()),
      ])),
      generators.repeat(generators.slow(corners.corners()), 10),
      generators.repeat(extend.extend(), 10),
      flatten.flatten(iterations = 10),
      generators.slow(snakes.snakes(frame_limit = 100)),
    ]))


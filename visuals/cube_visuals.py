from display import *
from .cube import *
import generators
from . import sides
from . import line
from . import rainbow
from . import transitions
from . import line_maps
from . import corners
from . import extend
from . import flatten
from . import snakes

def cube_visuals():
  return generators.sequence([
    generators.sequence([
      scroll_past(Cube(SIZE, Colour.red()), Direction.UP),
      scroll_past(Cube(SIZE, Colour.green()), Direction.RIGHT),
      scroll_past(Cube(SIZE, Colour.blue()), Direction.FRONT),
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
  ])

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, cube_visuals())


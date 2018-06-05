from display import *
from .cube import *
import generators
from . import edges
from . import faces
from . import line
from . import rainbow
from . import transitions
from . import line_maps
from . import corners
from . import extend
from . import flatten
from . import snakes
from . import matrix

def cube_visuals():
  return generators.sequence([
    generators.sequence([
      scroll_past(Cube(SIZE, Colour.red()), Direction.UP),
      scroll_past(Cube(SIZE, Colour.green()), Direction.RIGHT),
      scroll_past(Cube(SIZE, Colour.blue()), Direction.FRONT),
    ]),
    generators.repeat(faces.faces(), 10),
    generators.repeat(edges.edges(), 10),
    generators.fast(
      line_maps.line_to_cube(generators.sequence([
        line.scroll_in(line.rainbow()),
        line.scroll_out(line.rainbow()),
      ]))),
    generators.repeat(corners.corners(), 10),
    generators.repeat(extend.extend(), 5),
    flatten.flatten(iterations = 10),
    generators.frame_limit(snakes.snakes(), 300),
    generators.frame_limit(matrix.matrix(), 300),
  ])

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, cube_visuals())


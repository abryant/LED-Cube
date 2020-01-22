from display import *
from .cube import *
import generators
from . import corners
from . import edges
from . import extend
from . import faces
from . import fireworks
from . import flatten
from . import layers
from . import line
from . import line_maps
from . import matrix
from . import rainbow
from . import rope
from . import snakes
from . import spiral
from . import text
from . import transitions
from . import wave

def cube_visuals():
  return generators.sequence([
    generators.sequence([
      scroll_past(Cube(SIZE, Colour.red()), Direction.UP),
      scroll_past(Cube(SIZE, Colour.green()), Direction.RIGHT),
      scroll_past(Cube(SIZE, Colour.blue()), Direction.FRONT),
    ]),
    generators.repeat(faces.faces(), 10),
    generators.repeat(edges.edges(), 10),
    text.text("BRIGHT", [Colour.red(), Colour.green(), Colour.blue()]),
    generators.fast(
      line_maps.line_to_cube(generators.sequence([
        line.scroll_in(line.rainbow()),
        line.scroll_out(line.rainbow()),
      ]))),
    text.text("subtle", [Colour((Colour.brightness // 8, 0, 0)), Colour((0, Colour.brightness // 8, 0)), Colour((0, 0, Colour.brightness // 8))]),
    generators.repeat(corners.corners(), 10),
    generators.frame_limit(spiral.spiral(), 100),
    generators.repeat(extend.extend(), 3),
    generators.frame_limit(generators.slow(layers.layers(), frames = 4), 100),
    generators.frame_limit(wave.wave(), 100),
    generators.frame_limit(snakes.snakes(), 300),
    generators.frame_limit(matrix.matrix(), 300),
    generators.frame_limit(rope.rope(), 300),
    generators.repeat(fireworks.fireworks(), 10),
  ])

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, cube_visuals())


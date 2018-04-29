# TODO: visualizations
# snow: snowflakes falling onto a white base
# snake AI: an AI playing 3D snake
# waves: a multicoloured 3D sine waveform, rotating around the axes
# 2048: a 3D game of 2048 with LED brightness and colour indicating number, with cube rotations as moves (needs a rotation animation)
#
import generators
from display import *
from .position import *

def get_perpendicular_direction(dir1, dir2):
  if (dir1 == Direction.UP or dir1 == Direction.DOWN) and (dir2 == Direction.LEFT or dir2 == Direction.RIGHT):
    return Direction.FRONT
  if (dir1 == Direction.LEFT or dir1 == Direction.RIGHT) and (dir2 == Direction.UP or dir2 == Direction.DOWN):
    return Direction.FRONT
  if (dir1 == Direction.UP or dir1 == Direction.DOWN) and (dir2 == Direction.FRONT or dir2 == Direction.BACK):
    return Direction.RIGHT
  if (dir1 == Direction.FRONT or dir1 == Direction.BACK) and (dir2 == Direction.UP or dir2 == Direction.DOWN):
    return Direction.RIGHT
  if (dir1 == Direction.LEFT or dir1 == Direction.RIGHT) and (dir2 == Direction.FRONT or dir2 == Direction.BACK):
    return Direction.DOWN
  if (dir1 == Direction.FRONT or dir1 == Direction.BACK) and (dir2 == Direction.LEFT or dir2 == Direction.RIGHT):
    return Direction.DOWN
  raise ValueError(str(dir1) + " and " + str(dir2) + " are not perpendicular")

def convert_face_coordinates(face_dir, coord, layer):
  x, y = coord
  x_inv, y_inv = SIZE - 1 - x, SIZE - 1 - y
  layer_inv = SIZE - 1 - layer
  return {
    Direction.UP: Pos(x, layer, y),
    Direction.DOWN: Pos(x, layer_inv, y_inv),
    Direction.LEFT: Pos(layer, y, x),
    Direction.RIGHT: Pos(layer_inv, y, x_inv),
    Direction.BACK: Pos(x_inv, y, layer),
    Direction.FRONT: Pos(x, y, layer_inv),
  }[face_dir]

class Cube:

  def __init__(self, size = SIZE, colour = Colour.BLACK):
    self.grid = [[[colour for z in range(size)] for y in range(size)] for x in range(size)]
    self.size = size


  def from_colours(colours):
    assert len(colours) == (SIZE * SIZE * SIZE)
    result = Cube()
    for layer_index in range(SIZE):
      layer = colours[(layer_index * SIZE * SIZE):((layer_index + 1) * SIZE * SIZE)]
      if (layer_index % 2) == 0:
        layer.reverse()
      for line_index in range(SIZE):
        line = layer[(line_index * SIZE):((line_index + 1) * SIZE)]
        if (line_index % 2) == 0:
          line.reverse()
        result.grid[layer_index][line_index] = line
    return result


  def copy(self):
    other = Cube(size = self.size)
    other.grid = [[[self.grid[x][y][z] for z in range(self.size)] for y in range(self.size)] for x in range(self.size)]
    return other

  def __repr__(self):
    return repr(self.get_colours())

  def __str__(self):
    s = ""
    for x in range(SIZE):
      face = ""
      for y in range(SIZE):
        line = ""
        for z in range(SIZE):
          line += str(self.grid[x][y][z]) + ", "
        face += line + "\n"
      s += "x=" + str(x) + "\n" + face.replace("^", "  ")
    return s

  def get_colours(self):
    """Maps the cube to the 1D colour list that can be displayed on the cube

    This mapping is done based on the order in which each LED exists in sequence in the real cube.
    The first layer is ordered:
    16 15 14 13
     9 10 11 12
     8  7  6  5
     1  2  3  4
    The second layer reverses this ordering
    """
    result = []
    for layer_index, layer in enumerate(self.grid):
      layer_result = []
      for line_index, line in enumerate(layer):
        line_result = line[:]
        if (line_index % 2) == 0:
          line_result.reverse()
        layer_result += line_result
      if (layer_index % 2) == 0:
        layer_result.reverse()
      result += layer_result
    return result

  def set(self, pos, colour):
    self.grid[pos.x][pos.y][pos.z] = colour

  def get(self, pos):
    return self.grid[pos.x][pos.y][pos.z]

  def fill(self, startpos, endpos, colour):
    for x in range(startpos.x, endpos.x + 1):
      for y in range(startpos.y, endpos.y + 1):
        for z in range(startpos.z, endpos.z + 1):
          self.grid[x][y][z] = colour

  def clear(self):
    self.fill(Pos(0, 0, 0), Pos(SIZE - 1, SIZE - 1, SIZE - 1), Colour.BLACK)

  def fill_layer(self, direction, layer, colours):
    """Fills the given layer in the given direction with the given colour.

    As the layer number increases [0-3], the filled layer moves away from the given direction."""
    if type(colours) is Colour:
      colours = [[colours for i in range(SIZE)] for j in range(SIZE)]
    for i in range(SIZE):
      for j in range(SIZE):
        coords = convert_face_coordinates(direction, (i, j), layer)
        self.grid[coords.x][coords.y][coords.z] = colours[i][j]

  def get_layer(self, direction, layer):
    """Gets the given layer, as a 2D list of colours."""
    result = [[Colour.BLACK for i in range(SIZE)] for j in range(SIZE)]
    for i in range(SIZE):
      for j in range(SIZE):
        coords = convert_face_coordinates(direction, (i, j), layer)
        result[i][j] = self.grid[coords.x][coords.y][coords.z]
    return result

  def fill_line(self, line_direction, other_coords, colours):
    """Fills the given line with the given colours.

    The direction represents the direction that the line is pointing in.
    other_coords is a Pos that represents the other two coordinates, the component in line_direction is ignored."""
    if type(colours) is Colour:
      colours = [colours for i in range(SIZE)]
    cs = colours[:]
    line_direction_value = line_direction.value.x if line_direction.value.x != 0 else (line_direction.value.y if line_direction.value.y != 0 else line_direction.value.z)
    if line_direction_value < 0:
      cs.reverse()
    for i in range(SIZE):
      x = i if line_direction.value.x != 0 else other_coords.x
      y = i if line_direction.value.y != 0 else other_coords.y
      z = i if line_direction.value.z != 0 else other_coords.z
      self.grid[x][y][z] = cs[i]

  def get_line(self, line_direction, other_coords):
    """Gets the colours on the given line

    The direction represents the direction that the line is pointing in.
    other_coords is a Pos that represents the other two coordinates, the component in line_direction is ignored."""
    line_direction_value = line_direction.value.x if line_direction.value.x != 0 else (line_direction.value.y if line_direction.value.y != 0 else line_direction.value.z)
    cs = [Colour.BLACK for i in range(SIZE)]
    for i in range(SIZE):
      x = i if line_direction.value.x != 0 else other_coords.x
      y = i if line_direction.value.y != 0 else other_coords.y
      z = i if line_direction.value.z != 0 else other_coords.z
      cs[i] = self.grid[x][y][z]
    if line_direction_value < 0:
      cs.reverse()
    return cs

  def transform_colours(self, f):
    """Transforms all of the colours in the cube using f(colour)"""
    for x in range(SIZE):
      for y in range(SIZE):
        for z in range(SIZE):
          self.grid[x][y][z] = f(self.grid[x][y][z])

def scroll_in(cube, direction):
  result = Cube(cube.size)
  startpos = direction.value * -cube.size
  while True:
    for i in range(cube.size):
      for x in range(cube.size):
        for y in range(cube.size):
          for z in range(cube.size):
            newpos = startpos + (direction.value * i) + Pos(x, y, z)
            if newpos.is_in_bounds(cube.size):
              result.set(newpos, cube.get(Pos(x, y, z)))
      yield result.copy()
    result = Cube(cube.size)
    yield True

def scroll_out(cube, direction):
  while True:
    for i in range(cube.size):
      result = Cube(cube.size)
      for x in range(cube.size):
        for y in range(cube.size):
          for z in range(cube.size):
            newpos = (direction.value * (i+1)) + Pos(x, y, z)
            if newpos.is_in_bounds(cube.size):
              result.set(newpos, cube.get(Pos(x, y, z)))
      yield result.copy()
    yield True

def single_frame(cube):
  while True:
    yield cube
    yield True

def cycle(cube, direction):
  c = cube.copy()
  while True:
    for i in range(cube.size):
      for layer in range(cube.size):
        c.fill_layer(direction, (layer + i) % cube.size, cube.get_layer(direction, layer))
      yield c.copy()
    yield True

def scroll_past(cube, direction):
  return generators.sequence([scroll_in(cube, direction), single_frame(cube), scroll_out(cube, direction)])

def combine_cubes(cube_a, cube_b):
  c = cube_a.copy()
  for x in range(cube_a.size):
    for y in range(cube_a.size):
      for z in range(cube_a.size):
        p = Pos(x, y, z)
        if c.get(p) == Colour.BLACK:
          c.set(p, cube_b.get(p))
  return c

if __name__ == "__main__":
  with Display() as d:
    generators.generate(d, generators.sequence([
      scroll_past(Cube(SIZE, Colour.red()), Direction.UP),
      scroll_past(Cube(SIZE, Colour.green()), Direction.RIGHT),
      scroll_past(Cube(SIZE, Colour.blue()), Direction.FRONT),
    ]), delay = 0.5)


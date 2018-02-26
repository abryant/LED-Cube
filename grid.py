from config import SIZE
from display import *
from position import *
import generators
from colorsys import hsv_to_rgb
import random

class Grid:
  def __init__(self, size = SIZE):
    self.grid = [[Colour.BLACK for x in range(size)] for y in range(size)]
    self.size = size

  def copy(grid):
    g = Grid(size = grid.size)
    g.grid = [[grid.grid[y][x] for x in range(grid.size)] for y in range(grid.size)]
    return g

  def from_array(grid, size = SIZE):
    g = Grid(size = size)
    g.grid = grid
    return g

  def get_colours(self):
    result = []
    for line_index, line in enumerate(self.grid):
      line_result = line[:]
      if (line_index % 2) == 1:
        line_result.reverse()
      result += line_result
    result.reverse()
    return result

  def get(self, pos):
    return self.grid[pos.y][pos.x]

  def set(self, pos, colour):
    self.grid[pos.y][pos.x] = colour

  def fill_line(self, direction, line, colours):
    """Fills the given line in the given direction with the given colour.

    As the line number increases [0-3], the filled line moves away from the given direction."""
    if direction.value.z != 0:
      raise ValueError("Bad direction: " + str(direction))
    if type(colours) is Colour:
      colours = [colours for i in range(self.size)]
    for i in range(self.size):
      coords = Pos(i, line if direction in [Direction.UP, Direction.LEFT] else self.size - 1 - line, 0)
      if direction in [Direction.LEFT, Direction.RIGHT]:
        coords = Pos(coords.y, coords.x, 0)
      self.grid[coords.y][coords.x] = colours[i]

  def get_line(self, direction, line):
    """Gets the given line, as a list of colours."""
    result = [Colour.BLACK for i in range(self.size)]
    for i in range(self.size):
      coords = Pos(i, line if direction in [Direction.UP, Direction.LEFT] else self.size - 1 - line, 0)
      if direction in [Direction.LEFT, Direction.RIGHT]:
        coords = Pos(coords.y, coords.x, 0)
      result[i] = self.grid[coords.y][coords.x]
    return result


def scroll_in(grid, direction):
  if direction.value.z != 0:
    raise ValueError("Bad direction: " + str(direction))
  result = Grid(size = grid.size)
  startpos = direction.value * -grid.size
  while True:
    for i in range(grid.size):
      for x in range(grid.size):
        for y in range(grid.size):
          newpos = startpos + (direction.value * i) + Pos(x, y, 0)
          if newpos.is_in_bounds(grid.size):
            result.set(newpos, grid.get(Pos(x, y, 0)))
      yield result.copy()
    result = Grid(grid.size)
    yield True

def scroll_out(grid, direction):
  while True:
    for i in range(grid.size):
      result = Grid(grid.size)
      for x in range(grid.size):
        for y in range(grid.size):
          newpos = (direction.value * (i+1)) + Pos(x, y, 0)
          if newpos.is_in_bounds(grid.size):
            result.set(newpos, grid.get(Pos(x, y, 0)))
      yield result.copy()
    yield True

def single_frame(grid):
  while True:
    yield grid
    yield True


if __name__ == "__main__":
  with Display() as d:
    g = Grid()
    g.fill_line(Direction.UP, 0, Colour.GREEN)
    g.fill_line(Direction.DOWN, 0, Colour.RED)
    g.fill_line(Direction.LEFT, 0, Colour.BLUE)
    g.fill_line(Direction.RIGHT, 0, Colour.WHITE)
    g.grid[0][0] = Colour.RED
    d.display(g.get_colours())

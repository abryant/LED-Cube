from .cube import *
from display import *
import generators
import random

class Snake:
  def __init__(self, pos, colour):
    self.snake = [pos]
    self.colour = colour
    self.direction = random.choice([d for d in Direction])

  def can_advance(self, direction, avoid_positions):
    p = self.snake[0] + direction.value
    return p.is_in_bounds() and not p in avoid_positions

  def get_next_position(self, avoid_positions):
    """Chooses a direction to advance, and returns the next position.

    This can return None if there are no valid directions to advance, in which case the snake stays still."""
    if random.randint(0, 10) < 3 or not self.can_advance(self.direction, avoid_positions):
      alt_dirs = [d for d in Direction if self.can_advance(d, avoid_positions)]
      if len(alt_dirs) == 0:
        return None
      self.direction = random.choice(alt_dirs)
    return self.snake[0] + self.direction.value

  def advance(self, new_position, grow = False):
    self.snake.insert(0, new_position)
    if not grow:
      self.snake = self.snake[0:-1]

  def draw(self, cube):
    for p in self.snake:
      cube.set(p, self.colour)

def setup(number_of_snakes):
  snakes = [
      Snake(Pos(0, 0, 0), Colour.red()),
      Snake(Pos(SIZE - 1, 0, SIZE - 1), Colour.green()),
      Snake(Pos(0, SIZE - 1, SIZE - 1), Colour.blue()),
      Snake(Pos(SIZE - 1, SIZE - 1, 0), Colour.white()),
  ][:number_of_snakes]
  for i in range(SIZE):
    for s in snakes:
      avoid = [p for avoid_snake in snakes for p in avoid_snake.snake]
      p = s.get_next_position(avoid)
      if p is None:
        # Failed to set up correctly, retry randomly.
        return None
      s.advance(p, grow = True)
  return snakes

def snakes(frame_limit = None, number_of_snakes = 3):
  snakes = None
  while snakes is None:
    snakes = setup(number_of_snakes)
  i = 0
  while True:
    c = Cube()
    for s in snakes:
      s.draw(c)
    yield c
    i += 1
    if frame_limit is not None and i == frame_limit:
      i = 0
      yield True
    for s in snakes:
      avoid = [p for avoid_snake in snakes for p in avoid_snake.snake]
      p = s.get_next_position(avoid)
      if p is None:
        s.snake.reverse()
      else:
        s.advance(p)

def main():
  with Display() as d:
    generators.generate(d, generators.slow(snakes()))

if __name__ == "__main__":
  main()

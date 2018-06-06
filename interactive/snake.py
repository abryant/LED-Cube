from .interactive import *
from visuals.cube import *
from display import *
import random

class Game:
  def __init__(self):
    self.snake = [Pos(SIZE // 2, SIZE // 2, 1), Pos(SIZE // 2, SIZE // 2, 0)]
    self.make_fruit()
    self.direction = Direction.FRONT

  def make_fruit(self):
    all_positions = [Pos(x, y, z) for x in range(SIZE) for y in range(SIZE) for z in range(SIZE) if Pos(x, y, z) not in self.snake]
    if len(all_positions) > 0:
      self.fruit = random.choice(all_positions)
    else:
      self.fruit = None

  def draw(self):
    c = Cube()
    c.set(self.fruit, Colour.red())
    c.set(self.snake[0], Colour.white())
    for i, p in enumerate(self.snake[1:]):
      c.set(p, Colour((0, Colour.brightness - 0.8 * i * (Colour.brightness / (len(self.snake) - 1)), 0)))
    return c

  def get_next_position(self):
    return self.snake[0] + self.direction.value

  def can_advance(self):
    next_pos = self.get_next_position()
    return next_pos.is_in_bounds() and next_pos not in self.snake[:-1]

  def advance(self):
    self.snake.insert(0, self.get_next_position())
    if self.snake[0] == self.fruit:
      self.make_fruit()
    else:
      self.snake = self.snake[0:-1]

class Snake(Interactive):

  def run(self):
    while True:
      game = Game()
      self.clear_input()
      while True:
        yield wait_for_input(value = game.draw())
        yield from self.get_next_move(game)
        if not game.can_advance():
          break
        game.advance()
        if game.fruit is None:
          # Nowhere left to place fruit: player wins!
          break
      for i in range(5):
        yield wait_time(0.1, value = Cube(colour = (Colour.green() if game.fruit is None else Colour.red())))
        yield wait_time(0.1, value = Cube())

  def get_next_move(self, game):
    new_dir = self.get_input_direction()
    while new_dir is None or (new_dir.value + game.direction.value) == Pos(0, 0, 0):
      yield wait_for_input()
      new_dir = self.get_input_direction()
    game.direction = new_dir


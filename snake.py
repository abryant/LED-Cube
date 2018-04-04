from cube import *
from display import *
from keyboard import *
import random
import time

key_directions = {
    'w': Direction.BACK,
    'a': Direction.LEFT,
    's': Direction.FRONT,
    'd': Direction.RIGHT,
    'e': Direction.UP,
    'x': Direction.DOWN,
}

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
    c.set(self.fruit, Colour.RED)
    c.set(self.snake[0], Colour.WHITE)
    for i, p in enumerate(self.snake[1:]):
      c.set(p, Colour((0, 20 - i * (18 / (len(self.snake) - 1)), 0)))
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

def play_game(get_next_move):
  with Display() as d:
    keyboard = Keyboard()
    while True:
      game = Game()
      # consume any pending keyboard input
      keyboard.get_last_char(options = key_directions.keys())
      while True:
        d.display(game.draw().get_colours())
        game.direction = get_next_move(game, keyboard)
        if not game.can_advance():
          break
        game.advance()
        if game.fruit is None:
          # Nowhere left to place fruit: player wins
          break
      if game.fruit is None:
        print("YOU WIN!")
      print("score: " + str(len(game.snake)))
      for i in range(5):
        d.display(Cube(colour = (Colour.GREEN if game.fruit is None else Colour.RED)).get_colours())
        time.sleep(0.1)
        d.display(Cube().get_colours())
        time.sleep(0.1)

def get_next_move_time_based(game, keyboard):
  time.sleep(1)
  char = keyboard.get_last_char(options = key_directions.keys())
  if char != '':
    new_dir = key_directions[char]
    if (new_dir.value + game.direction.value) != Pos(0, 0, 0):
      return new_dir
  return game.direction

def get_next_move_turn_based(game, keyboard):
  while True:
    char = keyboard.wait_for_char(options = key_directions.keys())
    new_dir = key_directions[char]
    if (new_dir.value + game.direction.value) != Pos(0, 0, 0):
      return new_dir

if __name__ == "__main__":
  play_game(get_next_move = get_next_move_turn_based)

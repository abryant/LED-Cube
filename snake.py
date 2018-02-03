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
    self.fruit = random.choice(all_positions)

  def draw(self):
    c = Cube()
    c.set(self.fruit, Colour.RED)
    c.set(self.snake[0], Colour.WHITE)
    for i, p in enumerate(self.snake[1:]):
      c.set(p, Colour((0, 20 - i * (10 / (len(self.snake) - 1)), 0)))
    return c

  def get_next_position(self):
    return self.snake[0] + self.direction.value

  def can_advance(self):
    next_pos = self.get_next_position()
    return next_pos.is_in_bounds() and next_pos not in self.snake

  def advance(self):
    self.snake.insert(0, self.get_next_position())
    if self.snake[0] == self.fruit:
      self.make_fruit()
    else:
      self.snake = self.snake[0:-1]

def main():
  with Display('/dev/ttyUSB0') as d:
    keyboard = Keyboard()
    while True:
      game = Game()
      while True:
        d.display(game.draw().get_colours())
        time.sleep(1)
        char = keyboard.get_last_char(options = key_directions.keys())
        if char != '':
          new_dir = key_directions[char]
          if (new_dir.value + game.direction.value) != Pos(0, 0, 0):
            game.direction = new_dir
        if not game.can_advance():
          break
        game.advance()
      print("score: " + str(len(game.snake)))
      for i in range(5):
        d.display(Cube(colour = Colour.RED).get_colours())
        time.sleep(0.1)
        d.display(Cube().get_colours())
        time.sleep(0.1)


if __name__ == "__main__":
  main()

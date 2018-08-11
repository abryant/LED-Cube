from .interactive import *
from visuals.cube import *
from visuals.text import *
from display import *

class Write(Interactive):

  def run(self):
    self.clear_input()
    while True:
      yield wait_for_input(value = Cube())
      input = self.get_input()
      if input is not None:
        for f in text(input, [Colour.red(), Colour.green(), Colour.blue()]):
          if type(f) is bool:
            break
          yield wait_time(0.05, value = f)


from cube import *
from config import SIZE
from display import *

if __name__ == "__main__":
  with Display() as d:
    d.display([Colour((255, 255, 255)) for i in range(SIZE * SIZE * SIZE)])


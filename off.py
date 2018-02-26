from config import SIZE
from cube import *
from display import *

if __name__ == "__main__":
  with Display() as d:
    d.display([Colour.BLACK for i in range(SIZE * SIZE * SIZE)])


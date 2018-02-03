from cube import *
from display import *

if __name__ == "__main__":
  with Display('/dev/ttyUSB0') as d:
    d.display([Colour.BLACK for i in range(SIZE * SIZE * SIZE)])


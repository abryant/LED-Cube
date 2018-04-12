import requests
import sys
from display import *

def check_prefix(infile):
  first = infile.read(1)
  if first == b'':
    raise EOFError()
  if first == b'C':
    if infile.read(1) == b'U':
      if infile.read(1) == b'B':
        if infile.read(1) == b'E':
          if infile.read(1) == b':':
            return True
  return False

def process_line(infile, display):
  if check_prefix(infile):
    length = ((infile.read(1)[0] << 8) | infile.read(1)[0])
    data = infile.read(length * 3)
    colours = []
    for i in range(length):
      r = data[3*i]
      g = data[3*i + 1]
      b = data[3*i + 2]
      colours.append(Colour((r, g, b)))
    display.display(colours)
  c = infile.read(1)
  while c != b'\n' and c != b'':
    c = infile.read(1)
  if c == b'':
    raise EOFError()

def main(url):
  with Display() as d:
    try:
      r = requests.get(url, stream=True)
      while True:
        process_line(r.raw, d)
    except EOFError:
      print("End of stream - stopping.")
      pass

if __name__ == "__main__":
  main(sys.argv[1])


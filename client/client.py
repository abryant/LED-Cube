import requests
import sys
from display import *

def process_line(line, display):
  print("Received: " + repr(line))
  if len(line) > 7 and line.startswith(b'CUBE:'):
    length = ((line[5] << 8) | line[6])
    data = line[7:7+(3*length)]
    colours = []
    for i in range(length):
      r = data[3*i]
      g = data[3*i + 1]
      b = data[3*i + 2]
      colours.append(Colour((r, g, b)))
    display.display(colours)

def main(url):
  with Display() as d:
    r = requests.get(url, stream=True)
    for line in r.iter_lines():
      process_line(line, d)

if __name__ == "__main__":
  main(sys.argv[1])


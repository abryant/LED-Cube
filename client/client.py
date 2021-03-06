import requests
import sys
import urllib3
from time import sleep
from display import *

# This client connects to the server to display it on small LED cubes or lines of LEDs via display/display.py.
# This requires an arduino running arduino/led_controller.ino to be connected to /dev/ttyUSB0 at 115200 baud.
#
# On larger 8x8x8 cubes, this client isn't useful. They require an ESP8266 running one of the ESP8266 arduino programs.

def check_prefix(infile, first):
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
  c = infile.read(1)
  if check_prefix(infile, c):
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
    while True:
      try:
        r = requests.get(url, stream=True, timeout=120)
        while True:
          process_line(r.raw, d)
      except EOFError:
        print("End of stream - reconnecting in 10 seconds...")
        sleep(10)
      except urllib3.exceptions.ReadTimeoutError:
        print("Timeout while reading - reconnecting...")

if __name__ == "__main__":
  main(sys.argv[1])


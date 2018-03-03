from time import sleep
from colorsys import hsv_to_rgb
import config
from config import BRIGHTNESS, DISPLAY_FILE
import os

class Colour:
  def __init__(self, rgb):
    self.r, self.g, self.b = int(rgb[0]), int(rgb[1]), int(rgb[2])

  def fromFloats(rgb):
    return Colour((rgb[0]*255, rgb[1]*255, rgb[2]*255))

  def __repr__(self):
    return "[r:" + str(self.r) + ", g:" + str(self.g) + ", b:" + str(self.b) + "]"

  def __str__(self):
    return "[r:" + str(self.r) + ", g:" + str(self.g) + ", b:" + str(self.b) + "]"

  def __eq__(self, other):
    return self.r == other.r and self.g == other.g and self.b == other.b

  def __ne__(self, other):
    return not self.__eq__(other)

Colour.RED = Colour((BRIGHTNESS, 0, 0))
Colour.YELLOW = Colour((BRIGHTNESS, BRIGHTNESS, 0))
Colour.GREEN = Colour((0, BRIGHTNESS, 0))
Colour.CYAN = Colour((0, BRIGHTNESS, BRIGHTNESS))
Colour.BLUE = Colour((0, 0, BRIGHTNESS))
Colour.MAGENTA = Colour((BRIGHTNESS, 0, BRIGHTNESS))
Colour.BLACK = Colour((0, 0, 0))
Colour.WHITE = Colour((BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))

Colour.RED_HUE = 0
Colour.GREEN_HUE = 120
Colour.BLUE_HUE = 240

def hue_to_colour(hue, brightness=BRIGHTNESS):
  return Colour.fromFloats(hsv_to_rgb((hue % 360) / 360, 1, brightness / 255))

def open_read(path):
  f = open(path, 'rb')
  while True:
    l = f.readline()
    if l == b'READY\n':
      print("Starting...")
      return f

class Display:
  def __init__(self, path = DISPLAY_FILE):
    self.path = path
    os.system('stty -F ' + path + ' cs8 115200 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts')
    self.readfile = open_read(path)
    self.writefile = open(path, 'wb')

  def display(self, colours):
    data = bytearray(4 + 3 * len(colours))
    data[0] = ord('G')
    data[1] = ord('O')
    data[2] = ord(':')
    data[3] = len(colours) * 3
    for i in range(len(colours)):
      data[4+3*i] = colours[i].r
      data[4+3*i+1] = colours[i].g
      data[4+3*i+2] = colours[i].b
    self.writefile.write(data)
    self.writefile.flush()
    self.readfile.read(3)

  def __enter__(self):
    return self

  def __exit__(self, type, value, traceback):
    self.writefile.close()
    self.readfile.close()

if __name__ == "__main__":
  with Display() as d:
    cs = [Colour(hsv_to_rgb(i / 360, 1, 20)) for i in range(0, 360, 30)]
    print([str(c) for c in cs])
    while True:
      d.display(cs)
      cs = cs[1:] + [cs[0]]
      sleep(0.05)


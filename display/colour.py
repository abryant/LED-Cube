from colorsys import hsv_to_rgb
from .config import BRIGHTNESS

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
Colour.YELLOW_HUE = 60
Colour.GREEN_HUE = 120
Colour.CYAN_HUE = 180
Colour.BLUE_HUE = 240
Colour.MAGENTA_HUE = 300

Colour.ALL_HUES = [Colour.RED_HUE, Colour.YELLOW_HUE, Colour.GREEN_HUE, Colour.CYAN_HUE, Colour.BLUE_HUE, Colour.MAGENTA_HUE]

def hue_to_colour(hue, brightness=BRIGHTNESS):
  return Colour.fromFloats(hsv_to_rgb((hue % 360) / 360, 1, brightness / 255))


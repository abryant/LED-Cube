from colorsys import hsv_to_rgb
from .config import BRIGHTNESS

class Colour:
  brightness = BRIGHTNESS
  RED_HUE = 0
  YELLOW_HUE = 60
  GREEN_HUE = 120
  CYAN_HUE = 180
  BLUE_HUE = 240
  MAGENTA_HUE = 300
  ALL_HUES = [RED_HUE, YELLOW_HUE, GREEN_HUE, CYAN_HUE, BLUE_HUE, MAGENTA_HUE]

  def __init__(self, rgb):
    self.r, self.g, self.b = int(rgb[0]), int(rgb[1]), int(rgb[2])

  def from_floats(rgb):
    return Colour((rgb[0]*255, rgb[1]*255, rgb[2]*255))

  def __repr__(self):
    return "[r:" + str(self.r) + ", g:" + str(self.g) + ", b:" + str(self.b) + "]"

  def __str__(self):
    return "[r:" + str(self.r) + ", g:" + str(self.g) + ", b:" + str(self.b) + "]"

  def __eq__(self, other):
    return self.r == other.r and self.g == other.g and self.b == other.b

  def __ne__(self, other):
    return not self.__eq__(other)

  def red():
    return Colour((Colour.brightness, 0, 0))

  def yellow():
    return Colour((Colour.brightness, Colour.brightness, 0))

  def green():
    return Colour((0, Colour.brightness, 0))

  def cyan():
    return Colour((0, Colour.brightness, Colour.brightness))

  def blue():
    return Colour((0, 0, Colour.brightness))

  def magenta():
    return Colour((Colour.brightness, 0, Colour.brightness))

  def black():
    return Colour((0, 0, 0))

  def white():
    return Colour((Colour.brightness, Colour.brightness, Colour.brightness))

Colour.BLACK = Colour((0, 0, 0))

def hue_to_colour(hue, brightness=None):
  if brightness is None:
    brightness = Colour.brightness
  return Colour.from_floats(hsv_to_rgb((hue % 360) / 360, 1, brightness / 255))

def get_opposite_hue(hue):
  return (hue + 180) % 360


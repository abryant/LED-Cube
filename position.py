from enum import Enum
from config import SIZE

class Pos:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def is_in_bounds(self, size = SIZE):
    return self.x >= 0 and self.x < size and self.y >= 0 and self.y < size and self.z >= 0 and self.z < size

  def __add__(self, other):
    return Pos(self.x + other.x, self.y + other.y, self.z + other.z)

  def __sub__(self, other):
    return Pos(self.x - other.x, self.y - other.y, self.z - other.z)

  def __mul__(self, other):
    if type(other) is int:
      return Pos(self.x * other, self.y * other, self.z * other)
    return Pos(self.x * other.x, self.y * other.y, self.z * other.z)

  def __neg__(self):
    return Pos(-self.x, -self.y, -self.z)

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.z == other.z

  def __ne__(self, other):
    return not self.__eq__(other)

  def __str__(self):
    return "[" + str(self.x) + "," + str(self.y) + "," + str(self.z) + "]"

  def __repr__(self):
    return "[" + str(self.x) + "," + str(self.y) + "," + str(self.z) + "]"

class Direction(Enum):
  UP = Pos(0, -1, 0)
  DOWN = Pos(0, 1, 0)
  LEFT = Pos(-1, 0, 0)
  RIGHT = Pos(1, 0, 0)
  FRONT = Pos(0, 0, 1)
  BACK = Pos(0, 0, -1)


from enum import Enum
from display import SIZE

class Pos:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def is_in_bounds(self, size = SIZE):
    return self.x >= 0 and self.x < size and self.y >= 0 and self.y < size and self.z >= 0 and self.z < size

  def is_2d(self):
    return self.z == 0

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

def is_direction_positive(direction):
  return (direction == Direction.DOWN or direction == Direction.RIGHT or direction == Direction.FRONT)

def is_same_axis(dir1, dir2):
  return (abs(dir1.value.x) == abs(dir2.value.x)) and (abs(dir1.value.y) == abs(dir2.value.y)) and (abs(dir1.value.z) == abs(dir2.value.z))

def opposite_direction(direction):
  return [d for d in Direction if is_same_axis(d, direction) and d != direction][0]

def perpendicular_direction(dir1, dir2):
  return [d for d in Direction if not (is_same_axis(d, dir1) or is_same_axis(d, dir2))][0]

from .cube import *
from display import *
import socket
from time import sleep

def get_ip():
  ip_str = None
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
      s.connect(("bryants.eu", 2823))
      ip_str = s.getsockname()[0]
  except OSError:
    return None
  ip_strs = ip_str.split(".")
  if len(ip_strs) != 4:
    return None
  return [int(x) for x in ip_strs]

def get_ip_cube(ip):
  if ip is None:
    return Cube(colour = Colour.red())
  c = Cube()
  for i in range(4):
    for y in range(2):
      for x in range(4):
        bit = (y * 4) + x
        if (ip[i] >> bit) & 1 == 1:
          c.set(Pos(x, i, y), Colour.white())
  return c

if __name__ == "__main__":
  with Display() as d:
    while True:
      ip = get_ip()
      cube = get_ip_cube(ip)
      d.display(cube.get_colours())
      if ip is not None:
        break
      sleep(1)


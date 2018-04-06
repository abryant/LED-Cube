from .config import DISPLAY_FILE
import os

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


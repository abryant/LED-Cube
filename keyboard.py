import os
import sys
import termios
import atexit
from select import select

class Keyboard:
  def __init__(self):
    self.fd = sys.stdin.fileno()
    self.old_terminal = termios.tcgetattr(self.fd)
    self.new_terminal = termios.tcgetattr(self.fd)

    self.new_terminal[3] = self.new_terminal[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_terminal)

    atexit.register(self.reset_terminal)

    self.stdin_unbuffered = os.fdopen(self.fd, 'rb', buffering=0)

  def reset_terminal(self):
    termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_terminal)

  def get_char(self):
    read,_,_ = select([self.stdin_unbuffered], [], [], 0)
    if read != []:
      c = self.stdin_unbuffered.read(1)
      return c.decode('ascii')
    else:
      return ''

  def wait_for_char(self, options=None):
    while True:
      read,_,_ = select([self.stdin_unbuffered], [], [])
      if read != []:
        c = self.stdin_unbuffered.read(1)
        char = c.decode('ascii')
        if options is None or char in options:
          return char

  def get_last_char(self, options=None):
    char = ''
    while True:
      c = self.get_char()
      if c == '':
        break
      else:
        if options is None or c in options:
          char = c
    return char


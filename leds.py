from display import *
from time import sleep
from colorsys import hsv_to_rgb
import random

LEDS = 16

def rainbow(num_leds = LEDS, brightness = 20):
  return [Colour(hsv_to_rgb(i / 360, 1, brightness)) for i in range(0, 360, 360 // num_leds)]

def cycle(colours, dir=1):
  i = 0
  while True:
    yield colours
    colours = colours[-dir:] + colours[:-dir]
    i = (i + 1) % len(colours)
    if i == 0:
      yield True

def repeat(colours, num_leds = LEDS):
  return [colours[i % len(colours)] for i in range(num_leds)]

def fade(colours, ratio):
  return [Colour((colours[i].r * ratio, colours[i].g * ratio, colours[i].b * ratio)) for i in range(len(colours))]

def knight_rider(cycles, num_leds = LEDS):
  while True:
    colours = [Colour.BLACK for i in range(num_leds)]
    cycle = cycles
    i = 0
    dir = 1
    while True:
      colours = fade(colours, 0.7)
      colours[i] = Colour((64, 0, 0))
      yield colours
      i += dir
      if i == 0 or i == num_leds - 1:
        dir = -dir
        cycle -= 1
        if cycle == 0:
          break
    for i in range(8):
      colours = fade(colours, 0.7)
      yield colours
    yield True

def random_static(num_leds = LEDS, brightness=20):
  while True:
    yield [Colour(hsv_to_rgb(random.randint(0, 359) / 360, 1, random.randint(1, brightness))) for i in range(num_leds)]

def scroll_in(colours, dir=1):
  """Scrolls in colours from a direction, doesn't display the fully scrolled in state"""
  while True:
    cs = [Colour.BLACK for i in range(len(colours))]
    for i in range(len(colours)):
      if dir == 1:
        cs[:i] = colours[len(colours) - i:]
      else:
        cs[len(colours) - i:] = colours[:i]
      yield cs
    yield True

def scroll_out(colours, dir=1):
  """Scrolls out colours in a direction, doesn't display the initial state"""
  while True:
    cs = colours[:]
    for i in range(len(colours)):
      if dir == 1:
        cs[i] = Colour.BLACK
        cs[i+1:] = colours[:len(colours)-1-i]
      else:
        cs[len(colours)-1-i] = Colour.BLACK
        cs[:len(colours)-1-i] = colours[i+1:]
      yield cs
    yield True

def single_frame(colours):
  while True:
    yield colours
    yield True

def scroll_past(colours, dir=1):
  return sequence([scroll_in(colours, dir=dir), single_frame(colours), scroll_out(colours, dir=dir)])

def binary_count(num_leds = LEDS):
  i = 0
  while True:
    yield [Colour.BLACK if ((i >> l) & 0x1) == 0 else Colour((20, 20, 20)) for l in range(num_leds)]
    i += 1
    if i == (1 << num_leds):
      yield True
      i = 0

def reverse(gen):
  return (val[::-1] if type(val) is list else True for val in gen)

def mirror(gen):
  return (((val[::-1] + val[:]) if type(val) is list else True) for val in gen)

def shuffle(gens):
  while True:
    for val in gens[random.randint(0, len(gens) - 1)]:
      if type(val) is list:
        yield val
      else:
        break
    yield True

def generate(display, gen, delay=0.05):
  while True:
    for colours in gen:
      if type(colours) is list:
        display.display(colours)
        sleep(delay)

def repeat_gen(gen, times):
  while True:
    for i in range(times):
      for val in gen:
        if type(val) is list:
          yield val
        else:
          break
    yield True

def sequence(gens):
  while True:
    for i in range(len(gens)):
      for val in gens[i]:
        if type(val) is list:
          yield val
        else:
          break
    yield True

def debug(gen):
  for val in gen:
    if type(val) is list:
      print(val)
    else:
      break

if __name__ == "__main__":
  with Display('/dev/ttyUSB0') as d:
    generate(d, shuffle([
      mirror(reverse(binary_count(LEDS // 2))),
      knight_rider(10),
      scroll_past([Colour.RED for i in range(LEDS)]),
      scroll_past([Colour.GREEN for i in range(LEDS)]),
      scroll_past([Colour.BLUE for i in range(LEDS)]),
      scroll_past([Colour.CYAN for i in range(LEDS)], dir=-1),
      scroll_past([Colour.MAGENTA for i in range(LEDS)], dir=-1),
      scroll_past([Colour.YELLOW for i in range(LEDS)], dir=-1),
      sequence([
        scroll_in(rainbow()),
        repeat_gen(cycle(rainbow()), 5),
        repeat_gen(cycle(rainbow(), dir=-1), 5),
        scroll_out(rainbow(), dir=-1),
      ]),
    ]))


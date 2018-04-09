from time import sleep
import random

def get_colours(val):
  if callable(getattr(val, 'get_colours', None)):
    return val.get_colours()
  return val

def shuffle(gens):
  while True:
    for val in gens[random.randint(0, len(gens) - 1)]:
      if type(val) is bool:
        break
      yield val
    yield True

def transform(generator, transform_function):
  for val in generator:
    if type(val) is bool:
      yield val
    else:
      yield transform_function(val)

def generate(display, gen, delay=0.05):
  while True:
    for colours in gen:
      cs = get_colours(colours)
      if type(cs) is list:
        display.display(cs)
        sleep(delay)

def repeat(gen, times):
  while True:
    for i in range(times):
      for val in gen:
        if type(val) is bool:
          break
        yield val
    yield True

def sequence(gens, transition=None):
  prev = None
  while True:
    for i in range(len(gens)):
      if transition is not None and prev is not None:
        current = next(gens[i])
        if type(current) is bool:
          # zero-length generator, move to next one
          continue
        prev_transition = None
        for t in transition(prev, current):
          if prev_transition is not None:
            yield prev_transition
          prev_transition = t
        prev = prev_transition

      for val in gens[i]:
        if type(val) is bool:
          break
        if prev is not None:
          yield prev
        prev = val
    yield True

def reverse(gen):
  vals = []
  for val in gen:
    if type(val) is bool:
      for v in vals:
        yield v
      vals = []
      yield True
    else:
      vals.insert(0, val)
  for v in vals:
    yield v

def slow(gen, frames = 2):
  while True:
    for val in gen:
      if type(val) is bool:
        break
      for i in range(frames):
        yield val
    yield True

def debug(gen):
  for val in gen:
    if type(val) is bool:
      break
    print(val)

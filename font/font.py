from .font_arrays import font_arrays

def print_character(c):
  arr = font_arrays[c]
  for y in range(8):
    for x in range(8):
      print('X' if (arr[y] >> x) & 1 else ' ', end='')
    print('')

def draw_character(c, on, off):
  """Draws the character c into an 8x8 array[x][y], with pixels set to on and off."""
  arr = font_arrays[c]
  return [[(on if (arr[y] >> x) & 1 else off) for y in range(8)] for x in range(8)]


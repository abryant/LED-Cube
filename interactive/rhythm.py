from .interactive import *
from visuals.cube import *
from display import *
import random
import time
from visuals import corners, edges, faces, fireworks, matrix, rope, snakes, spiral, starfield, wave

ALL_TIMED_VISUALS = [faces.faces, fireworks.fireworks, edges.edges, corners.corners]
ALL_IDLE_VISUALS = [snakes.snakes, matrix.matrix, rope.rope, spiral.spiral, starfield.starfield, wave.wave]

ROLLING_AVERAGE_LENGTH = 3

MAX_VISUAL_ITERATIONS = 20
MAX_IDLE_FRAMES = 200

MIN_FRAME_DELAY = 0.05
IDLE_ANIMATION_DELAY = 0.05 # 20fps for idle animations

def median(delays):
  delays = delays[:]
  delays.sort()
  if len(delays) % 2 == 0:
    return (delays[(len(delays) // 2) - 1] + delays[len(delays) // 2]) / 2
  return delays[len(delays) // 2]

def clamp(n, min_n, max_n):
  return min(max_n, max(min_n, n))

class Rhythm(Interactive):

  def __init__(self):
    self.current_idle_animation = None
    self.current_idle_animation_function = None
    self.idle_frames = 0
    self.current_visual = None
    self.current_visual_function = None
    self.visual_iterations = 0
    super().__init__()

  def run(self):
    self.clear_input()
    last_beat_time = None
    last_delays = []
    last_delay_times = []
    visual_start_time = None
    visual_end_time = None
    current_frames = None
    while True:
      t = time.perf_counter()

      # Remove old beat delays.
      while (len(last_delay_times) > 0
          and t - last_delay_times[0] > median(last_delays) * (ROLLING_AVERAGE_LENGTH + 1)):
        last_delays = last_delays[1:]
        last_delay_times = last_delay_times[1:]
        if len(last_delays) == 0:
          last_beat_time = None

      if self.has_input():
        # Consume the input, no need to read it.
        self.get_input()
        if last_beat_time is None:
          last_beat_time = t
        elif t > last_beat_time:
          if len(last_delays) == ROLLING_AVERAGE_LENGTH:
            last_delays = last_delays[1:]
            last_delay_times = last_delay_times[1:]
          last_delays.append(t - last_beat_time)
          last_delay_times.append(t)
          last_beat_time = t

      # Stop an animation frame if the animation has ended
      if visual_end_time is not None and t >= visual_end_time:
        visual_start_time = None
        visual_end_time = None
        current_frames = None

      # Start an animation if none is playing and we have timing data
      if visual_start_time is None and len(last_delays) > 0:
        visual_start_time = t
        current_frames = self.get_visual_frames()
        visual_end_time = visual_start_time + median(last_delays)

      if visual_start_time is None:
        yield wait_for_input_or_time(IDLE_ANIMATION_DELAY, value = self.get_idle_frame())
      else:
        current_frame_index = self.get_frame_index(t, visual_start_time, visual_end_time, len(current_frames))
        next_frame_delay = (visual_end_time - visual_start_time) / len(current_frames)
        next_frame_delay = max(MIN_FRAME_DELAY, next_frame_delay)
        yield wait_for_input_or_time(next_frame_delay, value = current_frames[current_frame_index])

  def get_frame_index(self, t, visual_start_time, visual_end_time, len_frames):
    position = (t - visual_start_time) / (visual_end_time - visual_start_time)
    return clamp(int(position * len_frames), 0, len_frames - 1)

  def get_visual_frames(self):
    if self.current_visual is None:
      self.current_visual_function = random.choice([i for i in ALL_TIMED_VISUALS if i != self.current_visual_function])
      self.current_visual = self.current_visual_function()
    frames = []
    for f in self.current_visual:
      if type(f) is bool:
        break
      frames.append(f)
    self.visual_iterations += 1
    if self.visual_iterations >= MAX_VISUAL_ITERATIONS:
      self.current_visual = None
      self.visual_iterations = 0
    return frames

  def get_idle_frame(self):
    if self.current_idle_animation is None:
      self.current_idle_animation_function = random.choice([i for i in ALL_IDLE_VISUALS if i != self.current_idle_animation_function])
      self.current_idle_animation = self.current_idle_animation_function()
    result = None
    for f in self.current_idle_animation:
      if type(f) is not bool:
        result = f
        break
    self.idle_frames += 1
    if self.idle_frames >= MAX_IDLE_FRAMES:
      self.current_idle_animation = None
      self.idle_frames = 0
    return result


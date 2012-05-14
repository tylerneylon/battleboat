import subprocess

import board
import constants

def _play_sound(filename):
  try:
    subprocess.Popen(['mplayer', filename],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
  except:
    subprocess.Popen(['afplay', filename],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)

def play_sound_for_fire_result(result):
  sound = None
  if result[0] == board.Board.HIT:
    sound = 'boom'
  elif result[0] in (board.Board.MISS,
                     board.Board.ALREADY_GUESSED,
                     board.Board.OUT_OF_BOUNDS):
    sound = 'doh'
  elif result[0] == board.Board.SUNK:
    ship_size = constants.SHIPS[result[1]][1]
    if ship_size <= 2:
      sound = 'tiny_expl'
    elif ship_size == 3:
      sound = 'small_expl'
    elif ship_size == 4:
      sound = 'large_expl'
    elif ship_size >= 5:
      sound = 'giant_expl'
  if sound:
    _play_sound('%s.wav' % sound)

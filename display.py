# display.py
#
# Usage:
#  import display
#
#  d = display()
#  d.print_str("a str")
#

import curses
import time

# This is useful for debugging.
f = open('debug_log', 'w')

class display():
  # Set up the curses environment.
  def __init__(self):
    f.write('__init__\n')
    self.win = curses.initscr()
    curses.noecho()
    curses.cbreak()
    self.win.border()
    h, w = self.win.getmaxyx()
    # Set the title.
    title = " BattleBoat! "
    self.win.addstr(0, ((w - len(title)) // 2), title)
    # Set up the terminal portion of the screen as the
    # lower 10 lines.
    self.term = self.win.subwin(h - 10, 0)
    self.term.border()
    self.win.refresh()
    self.term.refresh()
    f.write('__init__ done\n')

  def __del__(self):
    f.write('__del__\n')
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    f.write('__del__ done\n')

  def print_str(self, s):
    f.write('print_str\n')
    self.term.addstr(1, 1, s)
    self.term.refresh()
  

if __name__ == '__main__':
  d = display()
  d.print_str('hello')
  time.sleep(1)

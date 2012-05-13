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
term_height = 10

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
    self.term = self.win.subwin(h - term_height, 0)
    self.term.setscrreg(1, term_height - 2)
    self.term.scrollok(True)
    self.term.border()
    self.win.refresh()
    self.term.refresh()

    # Keep track of our current position in the terminal.
    self.termline = 1

    f.write('__init__ done\n')

  def __del__(self):
    f.write('__del__\n')
    curses.nocbreak()
    curses.echo()
    curses.endwin()
    f.write('__del__ done\n')

  def print_str(self, s):
    f.write('print_str\n')
    self.term.addstr(self.termline, 1, s)
    self.termline += 1
    if self.termline == term_height - 1:
      try:
        self.term.scroll(1)
        self.term.border()
      except Exception, e:
        f.write('%s\n' % `e`)
      self.termline = term_height - 2 
    self.term.move(self.termline, 1)
    self.term.refresh()

  def input_str(self):
    pass
  

if __name__ == '__main__':
  d = display()
  slist = ['hi', 'there', 'how', 'are', 'you', 'fine', 'thanks', 'nice', 'of', 'you', 'to', 'ask']
  for s in slist:
    d.print_str(s)
    d.win.getch()
  time.sleep(2)


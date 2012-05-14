# display.py
#
# Usage:
#  import display
#
#  d = display.display()
#  d.print_str("a str")
#  s = d.input_str()
#
# TODO
#  Use constants.py
#  Make screen sizes more adaptive to the user's settings.
#


import board
import curses
import time

# This is useful for debugging.
f = open('debug_log', 'w')
term_height = 10

def _add_title(win, title):
  title = " %s " % title # Add padding around it.
  h, w = win.getmaxyx()
  win.addstr(0, ((w - len(title)) // 2), title)

class display():
  # Set up the curses environment.
  def __init__(self):
    f.write('__init__\n')
    self.win = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    self.win.border()
    _add_title(self.win, "BattleBoad!")

    # Set up the terminal portion of the screen as the
    # lower 10 lines.
    h, w = self.win.getmaxyx()
    self.term = self.win.subwin(h - term_height, 0)
    self.term.setscrreg(1, term_height - 2)
    self.term.scrollok(True)
    self.term.border()

    # Set up the ship and guess displays.
    self.shipwin = self.win.subwin(12, 22, 3, 3)
    self.shipwin.border()
    _add_title(self.shipwin, "My Ships")

    self.guesswin = self.win.subwin(12, 22, 3, 30)
    self.guesswin.border()
    _add_title(self.guesswin, "My Attacks")

    # Set up color pairs
    # TODO Use named constants for these color pairs.
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLACK)

    # Keep track of our current position in the terminal.
    self.termline = 1
    self.term.move(self.termline, 1)
    self.win.refresh()
    self.shipwin.refresh()
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
    self.term.addstr(self.termline, 1, s)
    self.termline += 1
    self._scroll_if_needed()

  def input_str(self):
    f.write('input_str\n')
    s = ''
    col = 1
    keep_going = True
    while keep_going:
      c = self.term.getch()
      keep_going = (c != ord('\n'))
      if keep_going:
        s += chr(c)
        self.term.addstr(self.termline, col, chr(c))
        col += 1
    self.termline += 1
    self._scroll_if_needed()
    return s

  def show_board(self, b):
    f.write('show_board\n')
    # Draw the boats.
    f.write('b.ships = %s\n' % `b.ships`)
    for x in xrange(10):
      for y in xrange(10):
        ship = b.ships[y][x]
        attr = curses.color_pair(1 if ship is not None else 2)
        s = ('%d-' % ship) if ship is not None else '  '
        self.shipwin.addstr(y + 1, 2 * x + 1, s, attr)

    # Draw the attacks on our ocean.
    f.write('b.ship_hit_map = %s\n' % `b.ship_hit_map`)
    for x in xrange(10):
      for y in xrange(10):
        attack = b.ship_hit_map[y][x]
        if attack is not None:
          self.shipwin.addstr(y + 1, 2 * x + 1, 'xx', curses.color_pair(1))

    # Draw the attacks on their ocean (aka guesses).
    for x in xrange(10):
      for y in xrange(10):
        guess = b.guesses[y][x]
        if guess is not None:
          s = 'xx' if guess else 'oo'
          self.guesswin.addstr(y + 1, 2 * x + 1, s, curses.color_pair(1))

    self.shipwin.refresh()
    self.guesswin.refresh()
    self.term.refresh()
    
    f.write('show_board done\n')

  def _scroll_if_needed(self):
    if self.termline == term_height - 1:
      self.termline = term_height - 2
      self.term.scroll(1)
      self.term.border()
    self.term.move(self.termline, 1)
    self.term.refresh()
  
if __name__ == '__main__':
  d = display()
  if True:
    slist = ['hi', 'there', 'how', 'are', 'you', 'fine', 'thanks', 'nice', 'of', 'you', 'to', 'ask']
    slist = ['hello', 'there'] # Shorter to test other things more.
    for s in slist:
      d.win.getch()
      d.print_str(s)
    s = d.input_str()
    d.print_str('I got the string %s' % s)
  b = board.Board()
  b.place_ship(0, 0, 0, board.Board.HORIZONTAL)
  b.place_ship(1, 1, 0, board.Board.HORIZONTAL)
  b.place_ship(2, 2, 0, board.Board.HORIZONTAL)
  b.place_ship(3, 3, 0, board.Board.HORIZONTAL)
  b.place_ship(4, 4, 0, board.Board.HORIZONTAL)
  b.fire_at(2, 2)
  b.fire_at(7, 7)
  b.record_guess_at(1, 1, True)
  b.record_guess_at(3, 4, False)
  f.write('about to show_board\n')
  d.show_board(b)
  time.sleep(3)


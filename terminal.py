#!/usr/bin/python

import board
import constants
import display
import sound

class Terminal(object):
  """Acts as the controller for BattleBoat"""
  
  def __init__(self):
    self.commands = {
       "help": self.print_help,
       "start": self.start_game,
       "test": self.test,
    }
    self.direction_to_const = {
       "horizontal": board.Board.HORIZONTAL,
       "vertical": board.Board.VERTICAL
    }
    self.ship_type_to_index = {}
    for i in range(0, len(constants.SHIPS)):
      self.ship_type_to_index[constants.SHIPS[i][0]] = i
    self.display = display.display()
  
  def output(self, my_str, new_line=True):
    self.display.print_str(my_str)
#    if new_line:
#      print my_str
#    else:
#      print my_str,
    
  def get_input(self):
    return self.display.input_str()
#    return raw_input()
  
  def run(self):
    answer = ""
    self.output("Welcome! Enter help to get help.")
    while answer not in ["N", "n"]:
      self.output(">>>", new_line=False)
      answer = self.get_input()
      if answer in self.commands:
        self.commands[answer]()
  
  def print_help(self):
    self.output("List of available commands:")
    self.output("  help - prints this message")
    self.output("  start - starts a new 2-player game")
    
  def start_game(self):
    self.output("Starting a new 2-player game.")
    self.output("Enter player A's name:", new_line=False)
    self.player_a_name = self.get_input()
    self.output("Enter player B's name:", new_line=False)
    self.player_b_name = self.get_input()
    self.boards = {
        self.player_a_name: board.Board(),
        self.player_b_name: board.Board()
    }
    
    # Enter ships for player A
    self.output(self.player_b_name + ", turn around! Hit enter when done.")
    self.get_input()
    self.enter_ships_for(self.player_a_name)
    self.output("")
    
    # Enter ships for player B
    self.output("Done!")
    self.output("Now, " + self.player_a_name +
                ", turn around! Hit enter when done.")
    self.get_input()
    self.enter_ships_for(self.player_b_name)
    
    self.play()
    
  def play(self):
    # Ping-play play for the game.
    self.output("Done!")
    self.output("Let's play the game.")
    player = self.player_a_name
    self.output(player + ", you got lucky! You start first.")
    while (not self.boards[self.player_a_name].all_ships_sunk() and
           not self.boards[self.player_a_name].all_ships_sunk()):
      self.play_turn(player)
      player = self._get_other_player(player)
    player = self._get_other_player(player)
    self.output("Congrats, " + player + ". You won!!!")
  
  def _get_other_player(self, player):
    if player == self.player_a_name:
      return self.player_b_name
    else:
      return self.player_a_name
  
  def play_turn(self, player):
    other_player = self._get_other_player(player)
    invalid_input = True
    while invalid_input:
      self.output(player + ", enter shoot coordinates: ", new_line=False)
      user_input = self.get_input().split(",")
      try:
        success, ship_type = self.boards[other_player].fire_at(
            int(user_input[0]),
            int(user_input[1]))
        sound.play_sound_for_fire_result((success, ship_type))
        if success == board.Board.OUT_OF_BOUNDS:
          self.output("Don't shoot outside the board!")
        elif success == board.Board.ALREADY_GUESSED:
          self.output("You already guess this one!")
        elif success == board.Board.MISS:
          self.output("You missed!")
          invalid_input = False
        elif success == board.Board.HIT:
          self.output("You hit something!")
          invalid_input = False
        elif success == board.Board.SUNK:
          self.output("Good job! You sank a " + constants.SHIPS[ship_type][0])
          invalid_input = False
      except Exception, e:
        self.output(str(e))
        self.output("Invalid input!")
    self.display.show_board(self.boards[player])

  def enter_ships_for(self, player_name):
    self.output(player_name + ", let's enter your ships.")
    self.output("For each ship, enter [x,y] coordinates and a direction. For "
                "example, for a ship starting at [1, 2] and placed "
                "horizontally, you need to enter 1,2,horizontal. "
                "Coordinates can be between 0 and 9 and direction is "
                "horizontal or vertical.")
    for ship_type, _ in constants.SHIPS:
      invalid_input = True
      while invalid_input:
        self.output(ship_type + ":", new_line=False)
        user_input = self.get_input().split(",")
        try:
          if not self.boards[player_name].place_ship(
              self.ship_type_to_index[ship_type],
              int(user_input[0]),
              int(user_input[1]),
              self.direction_to_const[user_input[2]]):
            self.output("Invalid input!")
          else:
            invalid_input = False
        except Exception, e:
          self.output(str(e))
          self.output("Invalid input!")
      self.display.show_board(self.boards[player_name])
    
  def test(self):
    """Sets up 2 test players and their boards."""
    self.player_a_name = "John"
    self.player_b_name = "Peter"
    self.boards = {}
    for player in (self.player_a_name, self.player_b_name):
      self.boards[player] = board.Board()
      self.boards[player].place_ship(0, 0, 0, 0)
      self.boards[player].place_ship(1, 1, 1, 0)
      self.boards[player].place_ship(2, 2, 2, 0)
      self.boards[player].place_ship(3, 3, 3, 0)
      self.boards[player].place_ship(4, 4, 4, 0)
    self.play()
    
    
def main():
  t = Terminal()
  t.run()

    
if __name__ == "__main__":
  main()

  
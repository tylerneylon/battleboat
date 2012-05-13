#!/usr/bin/python

import constants


class Terminal(object):
  """Acts as the controller for BattleBoat"""
  
  def __init__(self):
    self.commands = {
       "help": self.print_help,
       "start": self.start_game
    }
  
  def output(self, str, new_line=True):
    if new_line:
      print str
    else:
      print str,
    
  def get_input(self):
    return raw_input()
  
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
    self.ships = {}
    self.ships[self.player_a_name] = {}
    self.ships[self.player_b_name] = {}
    
    # Enter ships for player A
    self.output(self.player_b_name + ", turn around! Hit enter when done.")
    self.get_input()
    self.enter_ships_for(self.player_a_name)
    self.output("")
    
    # Enter ships for player B
    self.output("Done! Now, " + self.player_a_name +
                ", turn around! Hit enter when done.")
    self.get_input()
    self.enter_ships_for(self.player_b_name)
    import pprint; pprint.pprint(self.ships)
    
  def enter_ships_for(self, player_name):
    self.output(player_name + ", let's enter your ships.")
    self.output("For each ship, enter [x,y] coordinates and a direction. For "
                "example, for a ship starting at [1, 2] and placed "
                "horizontally, you need to enter 1,2,horizontal. "
                "Coordinates can be between 0 and 9 and direction is "
                "horizontal or vertical.")
    
    for ship_type, ship_size in constants.SHIPS:
      invalid_input = True
      while invalid_input:
        self.output(ship_type + ":", new_line=False)
        user_input = self.get_input().split(',')
        try:
          if (len(user_input) != 3 or
              int(user_input[0]) not in range(0, 10) or
              int(user_input[1]) not in range(0, 10) or
              user_input[2] not in ["horizontal", "vertical"]):
            # TODO:Also check for overlapping ships.
            self.output("Invalid input!")
          else:
            x, y, direction = user_input
            invalid_input = False
        except:
          self.output("Invalid input!")
      self.ships[player_name][ship_type] = (int(x), int(y), direction)
    

    
    
    
def main():
  t = Terminal()
  t.run()

    
if __name__ == "__main__":
  main()

  
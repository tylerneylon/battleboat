#!/usr/bin/python

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
    self.output(self.player_a_name + ", turn around! Hit enter when done.")
    self.output(self.player_a_name + ", let's enter your ships.")
    # Enter each ship type.
    
    
    
def main():
  t = Terminal()
  t.run()

    
if __name__ == "__main__":
  main()

  
import constants

class Board(object):
  # Ship directions.
  HORIZONTAL = 0
  VERTICAL = 1

  # Fire results.
  OUT_OF_BOUNDS = -2
  ALREADY_GUESSED = -1
  MISS = 0
  HIT = 1
  SUNK = 2

  def __init__(self):
    self.ships = [[None for _ in range(constants.BOARD_SIZE)]
                  for _ in range(constants.BOARD_SIZE)]
    self.guesses = [[None for _ in range(constants.BOARD_SIZE)]
                    for _ in range(constants.BOARD_SIZE)]
    self.ship_hit_map = [[None for _ in range(constants.BOARD_SIZE)]
                      for _ in range(constants.BOARD_SIZE)]
    self.ship_health = [ship[1] for ship in constants.SHIPS]
    self.placed_ships = [False for ship in constants.SHIPS]

  def fire_at(self, row, col):
    if not Board._is_in_bounds(row, col):
      return Board.OUT_OF_BOUNDS, None
    if self.ship_hit_map[row][col]:
      return Board.ALREADY_GUESSED, None
    ship_type = self.ships[row][col]
    if ship_type is not None:
      self.ship_hit_map[row][col] = True
      self.ship_health[ship_type] -= 1
      if self.ship_health[ship_type] == 0:
        return Board.SUNK, ship_type
      return Board.HIT, None
    return Board.MISS, None

  def all_ships_sunk(self):
    for ship_index in range(len(self.placed_ships)):
      if self.placed_ships[ship_index] and self.ship_health[ship_index]:
        return False
    return True

  def record_guess_at(self, row, col, hit):
    self.guesses[row][col] = hit

  def get_guess_at(self, row, col):
    return self.guesses[row][col]

  def place_ship(self, ship_type, start_row, start_col, direction):
    # Get ship.
    if ship_type < 0 or ship_type >= len(constants.SHIPS):
      return False
    if self.placed_ships[ship_type]:
      return False
    ship = constants.SHIPS[ship_type]

    # Find ending coordinates.
    if direction == Board.HORIZONTAL:
      end_row = start_row
      end_col = start_col + ship[1] - 1
    else:
      end_row = start_row + ship[1] - 1
      end_col = start_col

    # Check bounds.
    if (not Board._is_in_bounds(start_row, start_col) or
        not Board._is_in_bounds(end_row, end_col)):
      return False

    # Check if board is free.
    for row in range(start_row, end_row + 1):
      for col in range(start_col, end_col + 1):
        if self._check_hit(row, col):
          return False

    # Place ship.
    for row in range(start_row, end_row + 1):
      for col in range(start_col, end_col + 1):
        self.ships[row][col] = ship_type

    self.placed_ships[ship_type] = True
    return True

  def _check_hit(self, row, col):
    return self.ships[row][col] is not None

  @staticmethod
  def _is_in_bounds(row, col):
    return (row >= 0 and col >= 0 and
        row < constants.BOARD_SIZE and col < constants.BOARD_SIZE)

import unittest

import board
import constants

class TestBoard(unittest.TestCase):
  def setUp(self):
    self.board = board.Board()

  def test_place_ship(self):
    # OK.
    self.assertEquals(board.Board.PLACED_SHIP,
                      self.board.place_ship(1, 4, 5, board.Board.HORIZONTAL))
    self.assertTrue(self.board._check_hit(4, 5))
    self.assertTrue(self.board._check_hit(4, 6))
    self.assertTrue(self.board._check_hit(4, 7))
    self.assertFalse(self.board._check_hit(4, 8))
    self.assertFalse(self.board._check_hit(5, 5))

    # Out of bounds.
    self.assertEquals(board.Board.OUT_OF_BOUNDS,
                      self.board.place_ship(4, 0, 8, board.Board.HORIZONTAL))
    
    # Collide with another ship.
    self.assertEquals(board.Board.COLLISION,
                      self.board.place_ship(4, 3, 6, board.Board.VERTICAL))

    # Already placed ship.
    self.assertEquals(board.Board.ALREADY_PLACED,
                      self.board.place_ship(1, 4, 5, board.Board.HORIZONTAL))

    # Place second ship.
    self.assertEquals(board.Board.PLACED_SHIP,
                      self.board.place_ship(0, 5, 5, board.Board.VERTICAL))
    self.assertTrue(self.board._check_hit(6, 5))

  def test_fire(self):
    self.assertEquals(board.Board.PLACED_SHIP,
                      self.board.place_ship(1, 4, 5, board.Board.HORIZONTAL))
    self.assertEqual(self.board.OUT_OF_BOUNDS, self.board.fire_at(-2, -2)[0])
    self.assertEqual(self.board.MISS, self.board.fire_at(4, 4)[0])
    self.assertEqual(self.board.MISS, self.board.fire_at(4, 4)[0])
    self.assertEqual(self.board.HIT, self.board.fire_at(4, 5)[0])
    self.assertEqual(self.board.HIT, self.board.fire_at(4, 6)[0])
    self.assertFalse(self.board.all_ships_sunk())
    self.assertEqual((self.board.SUNK, 1), self.board.fire_at(4, 7))
    self.assertEqual(self.board.ALREADY_GUESSED, self.board.fire_at(4, 7)[0])
    self.assertTrue(self.board.all_ships_sunk())

if __name__ == '__main__':
    unittest.main()

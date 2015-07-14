"""Test ../src/board.py"""

import unittest
import numpy as np

from src import board

# Development notes:
# - Add more tests:
#    * make board with 0 or negative size
#    * test pattern by itself
#    * check_coordinates: does it take one, two, etc arguments well, list?
#    * add_cell --> success, outside, wrong player, 
#                    player on already owned but live cell
#    * add_cells --> actually works, complains if outside, complains if
#                    now owned, this one doesn't complain if put on owned
#                    but live (perhaps return the number of used cells, not
#                    counting the already live ones?), if actual pattern
#                    fits on map but non-trimmed does not!
#    * check the evolution works on some simple cases
# - Checking if proper exceptions etc are received.
#
# Questions:
# - why can we access board.np ?

class BoardTest(unittest.TestCase):

    # preparing to test
    def setUp(self):
        self.board = board.Board(2, 3)
     
    # ending the test
    def tearDown(self):
        # I guess nothing to do here
        pass
    
    # these tests work on the innards... bad!! ------------------------------
    def testEmptyBoard(self):
        self.assertTrue(np.all(self.board._board == 0)) 
     
    # these are proper public interface tests -------------------------------
    def testPlace(self):
        self.board.assign_territory(0,0,1)
        self.board.add_cell(0, 0, 1) # should go through
        self.assertRaises(board.IllegalActionException, 
                          self.board.add_cell(0, 0, 2))

    def testBlah(self):
        self.fail()
        # always fails

if __name__ == '__main__':
    unittest.main()

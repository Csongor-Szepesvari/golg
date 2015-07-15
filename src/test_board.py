"""Test ../src/board.py"""

import unittest
import numpy as np

import board

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
        self.board_sm = board.Board(3, 4)
        self.board_bi = board.Board(10, 12)
        self.pattern = board.Pattern(3, 2)
        self.pat_spec = (".O.",
                        "..O",
                        "OOO")
     
    # ending the test
    def tearDown(self):
        # I guess nothing to do here
        pass
    
    # these tests work on the innards... bad!! ------------------------------
    def testEmptyBoard(self):
        self.assertTrue(np.all(self.board_sm._board == 0)) 
     
    # these are proper public interface tests -------------------------------
    def testPlace(self):
        self.board_sm.assign_territory(0,0,1)
        self.board_sm.add_cell(0, 0, 1) # should go through
#        self.assertRaises(board.IllegalActionException, 
#                          self.board_sm.add_cell, 0, 0, 2)
        with self.assertRaises(board.IllegalActionException):    # newer way!
            self.board_sm.add_cell(0, 0, 2)
        

    # some tests purely for the patterns ------------------------------------
    def testPatternCenter(self):
        self.assertEqual( self.pattern.get_center(), [1,0] )
        
    def testPatternSlice(self):
        self.assertTrue(np.array_equal(self.pattern.get_slice(1, 2), 
                                       np.array( [[0, 2], [3, 4]])),
                        "The slice returned is not the expected one.")

    def testPatternLoadUnsupported(self):
        with self.assertRaises(ValueError):
            self.pattern.load(None, "myformat")

    def testLoadPlaintext(self):
        self.pattern.load(self.pat_spec, "plaintext")
        self.pattern.load_plaintext(self.pat_spec)

if __name__ == '__main__':
    unittest.main()

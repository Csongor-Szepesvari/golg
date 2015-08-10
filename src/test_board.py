"""Test ../src/board.py"""

import unittest
import numpy as np

import board

# Development notes:
# - Add more tests:
#    * check_coordinates: does it take one, two, etc arguments well, list?
#    * add_cell --> success, outside, wrong player, 
#                    player on already owned but live cell
#    * add_cells --> actually works, complains if outside, complains if
#                    now owned, this one doesn't complain if put on owned
#                    but live (perhaps return the number of used cells, not
#                    counting the already live ones?), if actual pattern
#                    fits on map but non-trimmed does not!
#    * check the evolution works on some simple cases
#
# Questions:
# - why can we access board.np ?

class BoardTest(unittest.TestCase):

    # preparing to test
    def setUp(self):
        self.board_sm = board.Board(4, 5)

        self.pattern = board.Pattern(3, 2)
        self.pat_spec_str = (".O.",
                             "..O",
                             "OOO")
        self.pattern_sp = board.Pattern(0,0)
        self.pattern_sp.load_plaintext(self.pat_spec_str)
        
        self.board_bi = board.Board(10, 12)
        self.board_bi.add_cells(2, 2, self.pattern_sp, 1, forced=True)
     
    # ending the test
    def tearDown(self):
        # I guess nothing to do here
        pass
    
    # these are proper public interface tests -------------------------------
    def testBadSetup(self):
        # note: we do not check 0 x 0
        with self.assertRaises(ValueError):
            board.Board(-12, -2)
        with self.assertRaises(ValueError):
            board.Board(4, -1)
        with self.assertRaises(ValueError):
            board.Board(-3, 12)
    
    def testPlace(self):
        self.board_sm.assign_territory(0,0,1)
        self.board_sm.add_cell(0, 0, 1) # should go through
#        self.assertRaises(board.IllegalActionException, 
#                          self.board_sm.add_cell, 0, 0, 2)
        with self.assertRaises(board.IllegalActionException):    # newer way!
            self.board_sm.add_cell(0, 0, 2)
        self.board_sm.add_cell(0, 0, 2, forced=True)
    
    def testCount(self):
        empty = self.board_sm.get_counts()
        self.assertEqual(empty, {})
        test2 = self.board_bi.get_counts()
        self.assertEqual(test2, {1: [5, 5]})
        self.board_bi.add_cell(9, 10, 3, forced=True)
        test3 = self.board_bi.get_counts()
        self.assertEqual(test3, {1: [5, 5], 3: [1,1]})
        self.board_bi.assign_territory(0, 7, 3)
        test4 = self.board_bi.get_counts()
        self.assertEqual(test4, {1: [5, 5], 3: [2,1]})
    
    def testAssignBadPattern(self):
        with self.assertRaises(board.IllegalActionException):
            self.board_sm.assign_territories(0, 0, self.pattern_sp, 1)

    def testAssignPattern(self):
        with self.assertRaises(board.IllegalActionException):
            self.board_sm.add_cell(3, 3, 1)
        self.board_sm.assign_territories(2, 2, self.pattern_sp, 1)
        self.board_sm.assign_territory(2, 3, 2)
        # should go through now
        self.board_sm.add_cell(3, 3, 1) 
        self.board_sm.add_cell(1, 2, 1) 
        self.board_sm.add_cell(3, 2, 1) 
        self.board_sm.add_cell(2, 3, 2) 
        # but these still don't
        with self.assertRaises(board.IllegalActionException):
            self.board_sm.add_cell(2, 3, 1)
        with self.assertRaises(board.IllegalActionException):
            self.board_sm.add_cell(2, 2, 1)
        

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
        self.pattern.load(self.pat_spec_str, "plaintext")
        self.pattern.load_plaintext(self.pat_spec_str)
        
    def testLoadPlaintextFile(self):
        self.pattern.load("patterns/glider.pat", "plaintext_file")
        self.pattern.load("patterns/block.pat", "plaintext_file")
        self.pattern.load("patterns/beehive.pat", "plaintext_file")
        self.pattern.load("patterns/blinker.pat", "plaintext_file")

    # these tests work on the innards... Expected to break sometimes ---------
    def testEmptyBoard(self):
        self.assertTrue(np.all(self.board_sm._board == 0)) 
     
    def testEvolveBasic1(self):
        self.board_sm.add_cell(1, 1, 1, forced=True)
        self.board_sm.add_cell(2, 3, 2, forced=True)
        self.board_sm.add_cell(3, 3, 2, forced=True)
        self.board_sm.evolve()
        expect = np.zeros(self.board_sm._board.shape)
        expect[1, 1] = -1
        expect[2, 2] = 2
        expect[2, 3] = -2
        expect[3, 3] = -2
        self.assertTrue( np.array_equal(self.board_sm._board, expect),
                         "Evolution did not go as expected")
        expect[2, 2] = -2
        self.board_sm.evolve()
        self.assertTrue( np.array_equal(self.board_sm._board, expect),
                         "Evolution did not go as expected")
        
    def testEvolveBasic2(self):
        self.fail("Note implemented yet")
        self.board_sm.add_cell(1, 1, 1, forced=True)
        self.board_sm.add_cell(2, 3, 2, forced=True)
        self.board_sm.add_cell(3, 3, 2, forced=True)
        self.board_sm.evolve()
        expect = np.zeros(self.board_sm._board.shape)
        expect[1, 1] = -1
        expect[2, 2] = 2
        expect[2, 3] = -2
        expect[3, 3] = -2
        self.assertTrue( np.array_equal(self.board_sm._board, expect),
                         "Evolution did not go as expected")
        expect[2, 2] = -2
        self.board_sm.evolve()
        self.assertTrue( np.array_equal(self.board_sm._board, expect),
                         "Evolution did not go as expected")


if __name__ == '__main__':
    unittest.main()

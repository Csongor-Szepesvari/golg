"""This file contains the Board class.

David and Csongor Szepesvari (c) 2015.

**This implementation will most definitely have to be switched out for 
a faster one**
"""

# imports here
import numpy as np




# Development notes here
# - lots to implement
# - bad implementation: pattern may have empty space on the side which could
#   technically be outside of the map, but current implementation doesn't
#   allow this!



class Board():
    """The Board class implements a 2D grid where each "pixel" is in one 
    of a number of states similarly to Conway's Game of Life, though 
    somewhat extended:

        * Dead
        * Dead, but owned by a player
        * Live, owned by a player

    Additionally, there may be features on the map, such as:
    
        * Resource
        * Wall
    
    **Note:** the game concepts are still under *heavy* development!
    """

    
#    Implementation details
#    ----------------------
#    1) at the moment we store each gridpoint as an integer with the following
#       interpretation. The integer, n, stored represents:
#           * |n| is the owner of the point (1 .. num of players, inclusive),
#           * n <= 0 means dead, n > 0 means alive.
#       In particular 0 is dead and not owned.
#    2) Convention: if method starts with "check", if check fail exception
#       is raised.
        
    def __init__(self, M, N):
        """Creates empty board of size M x N -- matrix notation"""
        # for good practice we declare *all* instance variables here
        self._board = np.zeros((M, N), dtype='=i4')     # integers
        self._M = M
        self._N = N
        # TODO later maybe make them directly accessible but read-only..
        self._timestep = 0

    def add_cell(self, i, j, player):
        Board._check_player(player)
        if self._board[i][j] is -player: # owned by player
            self._board[i][j] = player
        else:
            raise IllegalActionException("Attempting to add a live cell on \
                            land not owned by the player.")
            

    def add_cells(self, i, j, pattern, player):
        """Place the specified pattern for the given player onto the map
        centered at i, j."""
        Board._check_player(player)
        # check if the pattern can be placed at the location
        corns = pattern.get_slice()
        tl, br = (list(corns[0]), list(corns[1])) # top-left and bot-right
        self.check_coordinates(tl, br)
        boardslice = self._board[tl[0]:tl[1], br[0]:br[1]] 
        # note: this is a view, so modifies underlying data
        if np.any( np.abs(boardslice[pattern.pattern]) is not player):
            raise IllegalActionException("Attempting to place a pattern on \
                            land not owned by the player.")
        else:
            boardslice[pattern.pattern] = player # placed the pattern!
    
    # ----- utility functions ------
    
    def check_coordinates(self, *coords):
        """Take a list of coordinates (as 2-tuples/list), raise an
        IllegalActionException if any of them are off the map."""
        for co in coords:
            if co[0] < 0 or co[1] < 0 or co[0] >= self._M or co[1] >= self._N:
                raise IllegalActionException(
                            "Attempting to use a location outside of the map.")
    
    @staticmethod
    def _check_player(player):
        if player <= 0: raise ValueError("Player must be positive integer.")
        
        
        
class IllegalActionException(ValueError):
    """An action was attempted that cannot be carried out."""        
    pass
        
class Pattern():
    """Represents a pattern of pixels (contained in some rectangle).
    
    As a low level representation, access is direct to members:
    
        pattern -- numpy bool array
    
    Standardizes functionality like indexing w.r.t. pattern."""
    def __init__(self, M, N):
        self.pattern = np.zeros((M, N), dtype='b')
    
    def load(self, pat):
        """Load a pattern from some representation pat"""
        pass # TODO implement

    def get_center(self):
        """They `i` and `j` indices of what's considered the center of
        the pattern."""
        return [d//2 for d in self.pattern.shape]
        
    def get_slice(self, ci, cj):
        """Given we place the pattern with center at `(ci, cj)`, return
        the index slice taken for this pattern.
        
        Returned as numpy array [ [si, sj], [ei, ej] ].
        """
        c = np.array((ci, cj))
        s = c - self.pattern.shape//2
        e = s + self.pattern.shape
        return np.vstack((s, e))
        
#    def get_live(self, ci, cj):
#        """Gets a generator for the coordinates of turned on cells when 
#        `cx`, `cy` is taken to be the coordinates of the center
#        of the pattern.
#        """
#        is_, js_ = self.pattern.nonzero()
#        cmi, cmj = self.get_center()
#        return ((ci-cmi+i, cj-cmj+j) for (i,j) in zip(is_, js_))
#        # explanation for Csongor: zip (here) turns two equal length
#        #    lists into one list of tuples in the way you'd think it's natural
        


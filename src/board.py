"""This file contains the Board class.

David and Csongor Szepesvari (c) 2015.

**This implementation will most definitely have to be switched out for 
a faster one**
"""

# imports here
import numpy as np
from collections import defaultdict

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
        self._maxplayer = 0 # the largest indexed player added

    def assign_territory(self, i, j, player):
        self._use_player(player)
        if self._board[i][j] != player:
            self._board[i][j] = -player 

    def assign_territories(self, i, j, pattern, player):
        """Make the specified pattern shape, centered at `i`, `j`, owned 
        by the specified `player`.
        
        *Note:* The switch will always be made, even if the cells were
        originally owned by someone else - dead or alive. The state
        remains unchanged.
        """
        self._use_player(player)
        boardslice = self._get_pattern_slice(i, j, pattern)
        idx = np.nonzero(pattern.pattern & (boardslice != 1))
        boardslice[idx] = -player

    def add_cell(self, i, j, player, forced=False):
        """Add a live cell for the specified player at the specified
        location.
        
        If not forced (default), this raises an `IllegalActionException`
        if the location is not owned by the player. Otherwise we set the
        specified cell to be live and belonging to the player, no matter
        what.
        """
        self._use_player(player)
        if forced or self._board[i][j] == -player: # owned by player
            self._board[i][j] = player
        else:
            raise IllegalActionException("Attempting to add a live cell on land not owned by the player.")
            
    def add_cells(self, i, j, pattern, player, forced=False):
        """Like `add_cell`, but for a pattern that will be centered at
        `i`, `j` on the map."""
        self._use_player(player)
        boardslice = self._get_pattern_slice(i, j, pattern)
        # note: this is a view, so modifies underlying data
        if not forced and np.any( np.abs(boardslice[pattern.getinds()]) != player):
            raise IllegalActionException("Attempting to place a pattern on land not owned by the player.")
        else:
            boardslice[pattern.getinds()] = player 
            # placed the pattern! TODO is nonzero really necessary?
    
    def evolve(self):
        """Take one timestep according to the game rules."""
        self._timestep += 1
        # TODO finish

    def get_counts(self):
        """Return the number of owned and live cells for each player.
        
        This is in the form::
        
            {playernum: [owned, live], ...}
            
        As a defaultdict. Live cells contribute to the owned count too.
        """
        # TODO slow.. later keep it updated during evolution.
        counts = defaultdict(lambda: [0,0])
        i, j = np.nonzero(self._board)
        for el in range(i.size):
            val = self._board[i[el], j[el]]
            counts[abs(val)][0] += 1
            if val > 0:
                counts[abs(val)][1] += 1
        return counts
        
    def _use_player(self, player):
        """Like `_check_player`, but we record that we are using this
        player."""
        Board._check_player(player)
        self._maxplayer = max(self._maxplayer, player)

    # ----- utility functions ------

    def _get_pattern_slice(self, i, j, pattern):
        """Get a view of the board corresponding to placing the
        center of specified pattern at `i`, `j`. If not a valid location,
        raises `IllegalActionException`. Example::
        
            boardslice = self._get_pattern_slice(5, 3, my_pattern)
            
        Since `boardslice` is a view, changing it changes the board.
        """
        corns = pattern.get_slice(i, j)
        tl, br = (list(corns[0]), list(corns[1])) # top-left and bot-right
        self.check_coordinates(tl, br)
        return self._board[tl[0]:br[0], tl[1]:br[1]] 

    
    def check_coordinates(self, *coords):
        """Take a list of coordinates (as 2-tuples/list), raise an
        IllegalActionException if any of them are off the map."""
        for co in coords:
            if co[0] < 0 or co[1] < 0 or co[0] > self._M or co[1] > self._N:
                raise IllegalActionException("Attempting to use a location outside of the map.")
    
    @staticmethod
    def _check_player(player):
        """Check if the player is a valid player index."""
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
    
    def get_center(self):
        """The `i` and `j` indices inside the pattern of what's considered
        the center of the pattern."""
        return [(d-1)//2 for d in self.pattern.shape]
        
    def get_slice(self, ci, cj):
        """Given we place the pattern with center at `(ci, cj)`, return
        the index slice taken for this pattern.
        
        Returned as numpy array [ [si, sj], [ei, ej] ].
        """
        c = np.array((ci, cj))
        sh = np.array(self.pattern.shape)
        ce = np.array(self.get_center())
        s = c - ce
        e = s + sh
        return np.vstack((s, e))
        
    def getinds(self):
        """List locations of `True` -- basically calls nonzero"""
        return np.nonzero(self.pattern)
        
    def load(self, pat, fmt):
        """Load a pattern from the representation `pat` that has the given 
        format `fmt`. Current possibilities are 
        
            `{ "plaintext" }`
        
        *Note:* this can change the size of the pattern!
        """
        if fmt is "plaintext":
            self.load_plaintext(pat)
        else:
            raise ValueError("The specified format is not supported.")
        pass # TODO implement more?

    def load_plaintext(self, pattern):
        """ Sample pattern::
        
            .O.
            ..O
            OOO
        
        As a list of strings, each line being an individual entry. Each line
        needs to have the same length, though this is not checked.
        """
        self.pattern = np.zeros( (len(pattern), len(pattern[0])), dtype='b' )
        for i, l in enumerate(pattern):
            for j, c in enumerate(l):
                if c is '.':
                    pass
                elif c is 'O':
                    self.pattern[i, j] = True
                else:
                    raise ValueError("The specified pattern is not of the correct format. Encountered unexpected character {}".format(c) )
                
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
        


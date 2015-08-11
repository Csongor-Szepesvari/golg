"""This file contains the Board class.

David and Csongor Szepesvari (c) 2015.

**This implementation will most definitely have to be switched out for 
a faster one**. Some suggestions towards this:

* Use the C code that is linked from 
  ``http://pmav.eu/stuff/javascript-game-of-life-v3.1.1/``
* Store a different map for each person (my understanding is that the
  above implementation is like a sparse matrix?), collect propagation
  info that can then be used to determine who has majority.

TODO: how to handle the border?

"""

# imports here
import numpy as np
from collections import defaultdict

# Development notes here
#
# - lots to implement
# - bad implementation: pattern may have empty space on the side which could
#   technically be outside of the map, but current implementation doesn't
#   allow this!
#
#
#


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
        """Take one timestep according to the game rules. The rules are:
        
        * If a cell is currently live, it remains live iff it has
          (2 or 3) live neighbours,
        * If a cell is currently dead, it spawns a live one iff it
          has exactly 3 live neighbours.
            
        The owner of the new cell is the one with the majority number of
        neighbours -- the current owner does not matter. Whenever there is
        a tie the cell will be dead.
        """
        nextboard = np.copy(self._board)
        nextboard *= -np.sign(nextboard) # sets everything dead, with owner
        # simplest evolve solution: iterate over the array, check neighbours
        # for each location, counts will count number of live cells for each player
        counts = np.empty( self._maxplayer+1, dtype='=i4' ) # 0 is unowned - not counted!
        it = np.nditer(self._board, flags=['multi_index'], op_flags=['readonly'])
        while not it.finished:
            ci, cj = (it.multi_index[0], it.multi_index[1])
            counts.fill(0)
            for n in self.stream_neighbours(ci, cj):
                if self._board[n[0],n[1]] > 0:
                    counts[ self._board[n[0],n[1]] ] += 1
            # counts now has all the correct info
            
            # since the tie-breaking rule shortcircuits everything else, we
            # check that one first -- except if there's only one player involved
            if np.count_nonzero(counts) > 1:
                best_players = np.argpartition(counts, -2)[-2:]
                their_counts = counts[best_players]
                if their_counts[0] == their_counts[1]:
                    # this spot remains dead -- move to the next one
                    it.iternext() # move iteration ahead!!
                    continue
            # just sum number of live neighs and implement the above described rules
            num_alive = counts.sum()
            if it[0] > 0:
                if num_alive == 2 or num_alive == 3:
                    # was alive, still alive, mark with majority player
                    nextboard[ci, cj] = np.argmax(counts)
            else:
                if num_alive == 3:
                    # was dead, now alive, mark with majority player
                    nextboard[ci, cj] = np.argmax(counts)
            it.iternext() # move iteration ahead!!
        self._timestep += 1
        self._board = nextboard
        

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

    __DIRS = (  (-1, -1), (-1, 0), (-1, 1), \
                ( 0, -1),          ( 0, 1), \
                ( 1, -1), ( 1, 0), ( 1, 1) )
    def stream_neighbours(self, i, j):
        """Streams the coordinates of valid neighbours of the given index."""
        for d in Board.__DIRS:
            pi, pj = d[0]+i, d[1]+j
            if 0 <= pi and pi < self._M and 0 <= pj and pj < self._N:
                yield((pi, pj))
    
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
    def __init__(self):
        """Do NOT use this. Use one of the "factory methods"
        
        * :py:meth:`empty_pattern`
        * :py:meth:`load_pattern`
        
        """
        # for convention we declare all member variables
        self.pattern = None
        pass # nothing happens
    
    @classmethod
    def empty_pattern(cls, M, N):
        """Returns a new, empty instance of the given size."""
        toret = cls()
        toret.pattern = np.zeros((M, N), dtype='b')
        return toret
        
    @classmethod
    def load_pattern(cls, pat, fmt):
        """Returns a new instance with the specified pattern.
        
        The pattern is read from the representation `pat`, which has the
        specified format `fmt`. Current possibilities are 
        
            `{ "plaintext", "plaintext_file" }`
        
        
        The description of each of these formats is as follows:
        
        - `plaintext`: see :py:meth:`board.Pattern.load_plaintext`
        - `plaintext_file`: a path to a file that contains purely a line-
          by-line description of the pattern similar to the format in
          :py:meth:`board.Pattern.load_plaintext`. Lines with only
          whitespace are skipped.
        
        """
        toret = cls()
        toret.load(pat, fmt)
        return toret
    
    def get_center(self):
        """The `i` and `j` indices inside the pattern of what's considered
        the center of the pattern."""
        return [(d-1)//2 for d in self.pattern.shape]
        
    def get_slice(self, ci, cj):
        """Given we place the pattern with center at `(ci, cj)`, return
        the index slice required for this pattern.
        
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
        """Load a pattern into this instance.
        
        Otherwise similar to :py:meth:`load_pattern`.
        *Note:* this can change the size of the pattern!
        """
        if fmt is "plaintext":
            self.load_plaintext(pat)
        elif fmt is "plaintext_file":
            with open(pat, 'r') as pat_source:
                str_ = [line.strip() for line in pat_source if line.strip()]
                self.load_plaintext(str_)
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
        


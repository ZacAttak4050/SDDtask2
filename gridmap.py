""" This is to create an underlying gridmap to guide the animals
    using coordinates. This will not be the visual.
"""

from collections import defaultdict
from math import sqrt

class GridMap():
    """ A rectangular map consisting of grids that are xrows
    and xcols, some squares can be blocked off; the bases.
    """

    def __init__(self, xrows, xcols):
        self.xrows = xrows
        self.xcols = xcols
        self.map = [[0] * self.xcols for i in range(xrows)]
        """ "Lambda" creates an anonymous function. i.e, a function
             that does not need to be named.
        """
        self.blocked = defaultdict(lambda : False)

    def blocked_coord(self, coord, blocked = True):
        """ Sets the blocked coordinates for the bases.
            True for blocked and False for unblocked.
        """

        self.map[coord[0]][coord[1]] = blocked

        if blocked:
            self.blocked[coord] = True
        else:
            if coord in self.blocked:
                del self.blocked[coord]

    def compute_movement(self, coord1, coord2):
        """ Calculate/compute the cost to move from one coordinate
            to another one. The cost is represented as the Euclidean
            distance.
        """

        return sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

    def adjacent_coordinates(self, coord):
        """ Calculate the adject coordinates
        """

        slist = []

        for drow in (-1,0,1):
            for dcol in (-1,0,1):
                if drow == 0 and dcol == 0
                continue

                newrow = coord[0] + drow
                newcol = coord[1] + dcol
                if (    0 <= newrow <= self.xrows - 1 and
                        0 <= newcol <= self.xcols - 1 and
                        self.map[newrow][newcol] == 0):
                    slist.append((newrow, newcol))

        return slist

    def printme(self):
        for row in range(self.xrows):
            for col in range(self.xcols):

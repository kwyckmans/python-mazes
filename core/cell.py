from typing import Dict, List, Optional
from core.distances import Distances


class Cell:
    """Represents a single cell at location row, col in a grid representing a maze.

    A cell has a position (row, col) in a grid. It also has neighbours in the
     north, south, east and west directions.

    A dictionary interface to check if a given cell is linked to
     another cell is also provided.
    """

    def __init__(self, row: int, col: int) -> None:
        self.north: Optional["Cell"] = None
        self.south: Optional["Cell"] = None
        self.east: Optional["Cell"] = None
        self.west: Optional["Cell"] = None

        self.row = row
        self.col = col

        # FIXME: This could be a list. Either you have a link, and it's true,
        #   or you don't have a link and the item is not in the dict.
        #
        #   Testing whether a cell is a link is faster with a dict,
        #   but conceptually a list is a tad easier. Values are small,
        #   so shouldn't be a problem?
        self._links: Dict["Cell", bool] = {}

    def link_biderectional(self, cell: "Cell"):
        """Connects this cell to cell, and cell to this cell."""
        self._links[cell] = True
        cell.link(self)

    def link(self, cell: "Cell"):
        """Connects this cell to `cell`. Does not connect the cells in
        the other direction.
        """
        self._links[cell] = True

    def unlink(self, cell: "Cell"):
        """Severs the connection between this cell and `cell`."""
        self._links.pop(cell)

    def unlink_bidirectional(self, cell: "Cell"):
        """Severs the connection betwwn this cell and `cell` and in the other
        direction.
        """
        self._links.pop(cell)
        cell.unlink(self)

    @property
    def links(self) -> Dict["Cell", bool]:
        """Return all the cells linked to this one."""
        return self._links

    def is_linked(self, cell: Optional["Cell"]) -> bool:
        """Is cell connected to this one?"""
        return cell in self._links

    def neighbors(self) -> List["Cell"]:
        """Returns a list of neighbouring cells, if any."""
        neighbors: List["Cell"] = []
        if self.north:
            neighbors.append(self.north)
        if self.east:
            neighbors.append(self.east)
        if self.south:
            neighbors.append(self.south)
        if self.west:
            neighbors.append(self.west)

        return neighbors

    def __str__(self):
        return f"Cell ({self.row}, {self.col})"

    # TODO make this a property, for consistency with other classes
    def distances(self) -> Distances:
        distances = Distances(self)
        frontier: List["Cell"] = [self]

        while frontier:
            new_frontier: List["Cell"] = []

            for cell in frontier:
                for link in cell.links:
                    if link in distances:
                        continue

                    distances[link] = distances[cell] + 1
                    new_frontier.append(link)

            frontier = new_frontier

        return distances

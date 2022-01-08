from typing import Dict, List, Optional
from core.distances import Distances

class Cell:
    def __init__(self, row: int, col: int) -> None:
        self.north: Optional["Cell"] = None
        self.south: Optional["Cell"] = None
        self.east: Optional["Cell"] = None
        self.west: Optional["Cell"] = None

        self.row = row
        self.col = col
        self.links: Dict["Cell", bool] = {}

    def link(self, cell: "Cell", bidi: bool = True):
        self.links[cell] = True

        if bidi:
            cell.link(self, False)

    def unlink(self, cell: "Cell", bidi: bool = True):
        self.links.pop(cell)

        if bidi:
            cell.unlink(self, False)

    @property
    def get_links(self) -> Dict["Cell", bool]:
        return self.links

    def is_linked(self, cell: "Cell") -> bool:
        return cell in self.links

    def neighbors(self) -> List["Cell"]:
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

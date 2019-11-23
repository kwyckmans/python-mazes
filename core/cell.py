from typing import Dict, Type
from core.distances import Distances

class Cell:
    def __init__(self, row: int, col: int) -> None:
        self.north, self.south, self.east, self.west = None, None, None, None
        self.row = row
        self.col = col
        self.links = {}

    def link(self, cell, bidi: bool = True):
        self.links[cell] = True

        if bidi:
            cell.link(self, False)

    def unlink(self, cell, bidi: bool = True):
        self.links.pop(cell)

        if bidi:
            cell.unlink(self, False)

    @property
    def get_links(self) -> Dict[str,"Cell"]:
        return self.links

    def is_linked(self, cell: "Cell") -> bool:
        return cell in self.links

    def neighbors(self):
        neighbors = []
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
    def distances(self):
        distances = Distances(self)
        frontier = [self]

        while frontier:
            new_frontier = []

            for cell in frontier:
                for link in cell.links:
                    if link in distances:
                        continue

                    distances[link] = distances[cell] + 1
                    new_frontier.append(link)

            frontier = new_frontier

        return distances
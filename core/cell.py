from typing import Dict, Type


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


if __name__ == "__main__":
    cell = Cell(2, 2)
    cell2 = Cell(2, 3)
    cell.link(cell2)
    print(cell.links)
    print(cell.is_linked(cell=cell2))
    print(cell.neighbors())
    cell.unlink(cell2)
    print(cell.is_linked(cell2))

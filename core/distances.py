from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from core.cell import Cell


class Distances:
    """Gives distances for all cells linked to a starting cell.

    This datastructure starts at a `root` cell and gives the distance
    from all cells linked to the root to the root. So, root -> A -> B
    results in:
        cells[root] = 0
        cells[A] = 1
        cells[B] = 2

    TODO: Bulding the distances structure should probably happen here, and not in cell.
    """

    def __init__(self, root: "Cell") -> None:
        self.root: "Cell" = root
        self.cells: Dict["Cell", int] = {}
        self.cells[root] = 0

    def __getitem__(self, key: "Cell") -> int:
        return self.cells[key]

    def __setitem__(self, key: "Cell", val: int) -> None:
        self.cells[key] = val

    def __contains__(self, key: "Cell") -> bool:
        return key in self.cells

    def get_path_to(self, goal: "Cell") -> "Distances":
        """TODO: look this up in the book"""
        current = goal

        breadcrumbs = Distances(self.root)
        breadcrumbs[current] = self.cells[current]

        while current is not self.root:
            for neighbor in current.links:
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs[neighbor] = self.cells[neighbor]
                    current = neighbor
                    break

        return breadcrumbs

    @property
    def max(self) -> Tuple["Cell", int]:
        """Returns the cell, and how far away it is, furthest away from the root."""
        max_distance = 0
        max_cell = self.root

        for cell, distance in self.cells.items():
            if distance > max_distance:
                max_cell = cell
                max_distance = distance

        return (max_cell, max_distance)

    def get_cells(self):
        return self.cells.keys()

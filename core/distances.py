from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from core.cell import Cell


class Distances:
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
        max_distance = 0
        max_cell = self.root

        for cell, distance in self.cells.items():
            if distance > max_distance:
                max_cell = cell
                max_distance = distance

        return (max_cell, max_distance)

    def get_cells(self):
        return self.cells.keys()

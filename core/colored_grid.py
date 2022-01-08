from typing import Optional, Tuple
from core.distances import Distances
from core.grid import Grid
from core.cell import Cell


class ColoredGrid(Grid):
    def __init__(self, rows: int, cols: int):
        super().__init__(rows, cols)
        self.farthest: Optional[Cell] = None
        self.max: int = 0
        self._distances: Optional[Distances] = None

    def distances(self, distances: Distances):
        print(f"Setting distances {distances}")
        self._distances = distances
        self.farthest, self.max = distances.max

    def _color_of(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        if not self._distances or not cell in self._distances:
            return None

        distance: int = self._distances[cell]

        intensity: float = float((self.max - distance)) / self.max

        red = int(255 * intensity)
        green = 128 + int(127 * intensity)
        blue = 0 #128 + int(127 * intensity)

        # dark = int((255 * intensity))
        # bright = 128 + int(127* intensity)
        return (red, green, blue)

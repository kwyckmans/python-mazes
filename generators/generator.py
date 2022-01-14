from typing import Protocol
from core.grid import Grid


class Generator(Protocol):
    @staticmethod
    def on(grid: Grid) -> Grid:
        return grid

import random
from core.grid import Grid


class BinaryTree:
    @staticmethod
    def on(grid: Grid) -> Grid:
        for cell in grid:
            neighbors = []
            if cell.north:
                neighbors.append(cell.north)
            if cell.east:
                neighbors.append(cell.east)

            if neighbors:
                neighbor = random.choice(neighbors)

            if neighbor:
                cell.link(neighbor)

        return grid

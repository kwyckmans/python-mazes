from core.distance_grid import DistanceGrid
from generators.binary_tree import BinaryTree

grid = DistanceGrid(10, 10)
BinaryTree.on(grid)

start = grid[0][0]
distances = start.distances()

grid.distances = distances
print(grid)

grid.distances = distances.get_path_to(grid[grid.nr_rows - 1][7])
print(grid)

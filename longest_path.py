from core.distance_grid import DistanceGrid
from generators.binary_tree import BinaryTree

grid = DistanceGrid(5, 5)
BinaryTree.on(grid)

start = grid[0][0]

print(start)

distances = start.distances()
new_start, distance = distances.max

print(new_start, distances)

new_distances = new_start.distances()
goal, distance = new_distances.max

grid.distances = new_distances.get_path_to(goal)
print(grid)

from core.distance_grid import DistanceGrid
from generators.binary_tree import BinaryTree

# Generate a random grid
grid = DistanceGrid(10, 10)
BinaryTree.on(grid)

# Generate distance map from a given starting point
start = grid[0][0]
distances = start.distances()

# Get the point furthest away from your initial starting point
new_start, distance = distances.max

# Get distancees from this distant point
new_distances = new_start.distances()

# Get the point that is furthest away, and as such is the longest path in the grid
goal, distance = new_distances.max

grid.distances = new_distances.get_path_to(goal)
print(grid)

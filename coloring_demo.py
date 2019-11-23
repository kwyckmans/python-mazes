from core.colored_grid import ColoredGrid
from generators.binary_tree import BinaryTree

grid = ColoredGrid(50,50)
BinaryTree.on(grid)

start = grid[0][0]

grid.distances(start.distances())

image = grid.to_png()
image.save("results/colorize.png")

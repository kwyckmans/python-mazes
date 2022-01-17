from typing import List
from core.colored_grid import ColoredGrid
from PIL.Image import Image

# from tqdm import tqdm

# from generators.binary_tree import BinaryTree
from generators.sidewinder import Sidewinder

grid = ColoredGrid(25, 25)
Sidewinder.on(grid)

# - start = grid[grid.rows / 2, grid.columns / 2]
start = grid[int(grid.nr_rows / 2)][int(grid.nr_cols / 2)]
# start = grid[0][0]

images: List[Image] = []
# TODO: This updates the colors of the gif based on the distance map. So colors are updated along the way.
#   I could also generate the final distance map and just animate the coloring. So, instead of to_png() I'd
#   have a to_gif, that just animates the colors based on the final distances. Would be more efficient.
for distances in start.distances_stepwise():
    # print("visualising distance")
    grid.distances(distances)
    images.append(grid.to_png())
    # image.save(f"results/animated_{frame_counter}.png")

images[0].save(
    "results/dijkstra.gif",
    save_all=True,
    append_images=images[1:],
    optimize=True,
    duration=20,
)

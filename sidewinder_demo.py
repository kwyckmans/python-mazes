from core.grid import Grid
from generators.sidewinder import Sidewinder

if __name__ == "__main__":
    grid = Grid(100, 100)
    Sidewinder.on(grid)

    image = grid.to_png()
    image.save("results/sidewinder.png")

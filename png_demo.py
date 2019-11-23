import sys
# sys.path.append("./core")
# sys.path.append("./generators")

from core.grid import Grid

if __name__ == "__main__":
    grid = Grid(2,2)

    image = grid.to_png()

    image.save("results/png_test.png")
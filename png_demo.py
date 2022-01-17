from core.grid import Grid

if __name__ == "__main__":
    grid = Grid(10, 10)

    image = grid.to_png()
    image.save("results/png_test.png")

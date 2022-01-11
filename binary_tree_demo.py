from generators.binary_tree import BinaryTree
from core.grid import Grid

if __name__ == "__main__":
    grid = Grid(10, 10)
    BinaryTree.on(grid)

    print(grid)
    image = grid.to_png()

    image.save("results/binary_tree.png")

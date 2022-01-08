from random import randrange
from timeit import default_timer as timer
from typing import Iterator, Optional

from PIL import Image, ImageDraw

from core.cell import Cell


class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        self.cells = [self.Row(row, cols) for row in range(0, rows)]
        self.nr_rows = rows
        self.nr_cols = cols
        self._configure_cells()

    def get(self, row: int, col: int) -> Optional[Cell]:
        if row < 0 or row >= len(self.cells):
            return None  # This returns None, since that makes setting up cell neighbours easier.

        if col < 0 or col >= len(self.cells[0]):
            return None

        return self.cells[row][col]

    @property
    def rows(self):
        for row in self.cells:
            yield row

    @property
    def random_cell(self):
        row = randrange(self.nr_rows)
        col = randrange(self.nr_cols)

        yield self.get(row, col)

    def __len__(self):
        return self.nr_rows * self.nr_cols

    def __getitem__(self, row: int) -> "Row":
        return self.cells[row]

    def __iter__(self) -> "Grid":
        self.row = 0
        self.col = -1
        return self

    def __next__(self):
        if (self.row == self.nr_rows - 1) and (self.col == self.nr_cols - 1):
            raise StopIteration

        if self.col == self.nr_cols - 1:
            self.col = -1
            self.row = self.row + 1

        self.col = self.col + 1
        return self.cells[self.row][self.col]

    def get_cells(self) -> Iterator[Cell]:
        """Returns a generator that loops over all contained cells.

        Same basic functionality as __iter__ and __next__, but using a generator.
        Difference being, this can only be used ONCE.
        """
        for row in self.cells:
            for c in row:
                yield c

    def _configure_cells(self) -> None:
        for cell in self:
            row, col = cell.row, cell.col

            cell.north = self.get(row - 1, col)
            cell.south = self.get(row + 1, col)
            cell.west = self.get(row, col - 1)
            cell.east = self.get(row, col + 1)

    def _contents_of(self, cell: Cell) -> str:
        return ""

    def _color_of(self, cell: Cell):
        return (255, 255, 255)

    def to_png(self, cell_size: int = 10, line_width: int = 1) -> Image.Image:
        img_width = self.nr_cols * cell_size + line_width
        img_height = self.nr_rows * cell_size + line_width

        BACKGROUND = (255, 255, 255)
        WALL = (0, 0, 0)

        image = Image.new("RGBA", (img_width, img_height), BACKGROUND)
        draw = ImageDraw.Draw(image)

        # TODO: figure out a cleaner way to do this
        modes = [
            "BACKGROUNDS",
            "WALLS",
        ]  # Currently, the order matters, otehrwise backgrounds will paint over walls

        for mode in modes:
            print(f"Mode: {mode}")
            for cell in self:
                x1 = cell.col * cell_size
                y1 = cell.row * cell_size
                x2 = (cell.col + 1) * cell_size
                y2 = (cell.row + 1) * cell_size

                if mode == "BACKGROUNDS":

                    color = self._color_of(cell)
                    draw.rectangle((x1, y1, x2, y2), fill=color)
                else:
                    if not cell.north:
                        draw.line([(x1, y1), (x2, y1)], WALL, line_width)
                    if not cell.west:
                        draw.line([(x1, y1), (x1, y2)], WALL, line_width)

                    if not cell.is_linked(cell.east) or not cell.east:
                        draw.line([(x2, y1), (x2, y2)], WALL, line_width)

                    if not cell.is_linked(cell.south) or not cell.south:
                        draw.line([(x1, y2), (x2, y2)], WALL, line_width)

        return image

    def __str__(self):
        result = "+" + "---+" * self.nr_cols + "\n"

        for row in self.cells:
            top = "|"
            bottom = "+"

            for cell in row:
                body = f" {self._contents_of(cell)} "

                if cell.east and cell.is_linked(cell.east):
                    east_boundary = " "
                else:
                    east_boundary = "|"

                top += body + east_boundary

                if cell.south and cell.is_linked(cell.south):
                    south_boundary = "   "
                else:
                    south_boundary = "---"

                corner = "+"
                bottom += south_boundary + corner

            result += top + "\n"
            result += bottom + "\n"

        return result

    class Row:
        def __init__(self, row, cols) -> None:
            self.cells = [Cell(row, col) for col in range(0, cols)]
            self.index = -1

        def __getitem__(self, col) -> Cell:
            if col < 0 or col >= len(self.cells):
                return None

            return self.cells[col]

        def __iter__(self):
            self.index = -1
            return self

        def __next__(self):
            if self.index == len(self.cells) - 1:
                raise StopIteration

            self.index = self.index + 1
            return self.cells[self.index]

        def __len__(self):
            return len(self.cells)


if __name__ == "__main__":
    grid = Grid(10, 10)

    i = 0

    start = timer()
    for cell in grid:
        i = i + 1
    end = timer()
    print(f"iterator run time: {end - start}")

    start = timer()
    for cell in grid.get_cells():
        i = i + 1
    end = timer()
    print(f"generator run time: {end - start}")

    print(f"cell at [2][3]: {grid[2][3]}")

    for i in range(0, 100):
        next(grid.random_cell)

    print(len(grid))

from random import randrange
from typing import Dict, Optional, Tuple

from PIL import Image, ImageDraw

from core.cell import Cell


class Grid:
    """A grid representing a maze"""

    def __init__(self, rows: int, cols: int) -> None:
        self.cells = {
            row: {col: Cell(row, col) for col in range(0, cols)} for row in range(0, rows)
        }
        # self.cells = [self.Row(row, cols) for row in range(0, rows)]
        self.nr_rows = rows
        self.nr_cols = cols
        self._row = 0
        self._col = -1
        self._configure_cells()

    def _configure_cells(self) -> None:
        for c in self:
            row, col = c.row, c.col

            if (row - 1, col) in self:
                c.north = self[row - 1][col]

            if (row + 1, col) in self:
                c.south = self[row + 1][col]

            if (row, col - 1) in self:
                c.west = self[row][col - 1]

            if (row, col + 1) in self:
                c.east = self[row][col + 1]

    @property
    def rows(self):
        for row in self.cells:
            yield row

    @property
    def random_cell(self):
        row = randrange(self.nr_rows)
        col = randrange(self.nr_cols)

        yield self[row][col]

    def __len__(self):
        return self.nr_rows * self.nr_cols

    def __getitem__(self, row: int) -> Dict[int, Cell]:
        """
        TODO: Replace this with __getitem__(self, row: Tuple[int, int]).
          See ndarray from numpy for inspiration. Then you can access cells
          with grid[row, col] instead of grid[row][col]. Allowing for accessor
          checks and so on in here. The book hints at funkier accessors down the line.

          On the other hand we want to have a way to return cells 'per row' for the
          Sidewinder algorithm. The book uses a `each_row` method.
          I also have the rows() property that does this.
        """
        return self.cells[row]

    def __iter__(self) -> "Grid":
        self._row = 0
        self._col = -1
        return self

    def __next__(self) -> Cell:
        if (self._row == self.nr_rows - 1) and (self._col == self.nr_cols - 1):
            raise StopIteration

        if self._col == self.nr_cols - 1:
            self._col = -1
            self._row = self._row + 1

        self._col = self._col + 1
        return self.cells[self._row][self._col]

    def __contains__(self, key: Tuple[int, int]):
        """
        TODO: Expecting a tuple here is not great. I should handle the case where it's
            not better. A check for type would already be better than nothing.
        """
        row, col = key
        return row in self.cells and col in self.cells[row]

    def _contents_of(self, cell: Cell) -> str:
        return " "

    def _color_of(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        return None

    def to_png(self, cell_size: int = 10, line_width: int = 1) -> Image.Image:
        """Renders the state of the grid to a PNG

        TODO: Should this be a `render` method, that takes in a renderer?
        """
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
            # print(f"Mode: {mode}")
            for cell in self:
                x1 = cell.col * cell_size
                y1 = cell.row * cell_size
                x2 = (cell.col + 1) * cell_size
                y2 = (cell.row + 1) * cell_size

                if mode == "BACKGROUNDS":
                    color: Optional[Tuple[int, int, int]] = self._color_of(cell)
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

            for _, cell in self[row].items():
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


if __name__ == "__main__":
    grid = Grid(10, 10)

    i = 0

    for i in range(0, 100):
        next(grid.random_cell)

    print(len(grid))

from typing import Optional
from core.distances import Distances
from core.grid import Grid
from core.cell import Cell


class DistanceGrid(Grid):
    def __init__(self, rows: int, cols: int):
        super().__init__(rows, cols)

        self.distances: Optional[Distances] = None

    def _contents_of(self, cell: Cell) -> str:
        # Pylint can't handle membership tests and optionals:

        if (
            self.distances
            and cell in self.distances  # pylint: disable=unsupported-membership-test
        ):
            return base36encode(
                self.distances[cell]  # pylint: disable=unsubscriptable-object
            )

        return super()._contents_of(cell)


def base36encode(number: int, alphabet: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """Converts an integer to a base36 string.

    Taken from https://stackoverflow.com/questions/1181919/python-base-36-encoding
    """
    base36 = ""
    sign = ""

    if number < 0:
        sign = "-"
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36

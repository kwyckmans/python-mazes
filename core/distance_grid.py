from core.grid import Grid
from core.cell import Cell

class DistanceGrid(Grid):
    def __init__(self, rows:int, cols:int):
        super().__init__(rows, cols)

        self.distances = None

    def _contents_of(self, cell:Cell) -> str:
        if self.distances and cell in self.distances:
            return base36encode(self.distances[cell])
        else:
            return super()._contents_of(cell)


# Taken from https://stackoverflow.com/questions/1181919/python-base-36-encoding
def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    """Converts an integer to a base36 string."""
    if not isinstance(number, int):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36
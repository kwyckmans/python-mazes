from core.grid import Grid

class ColoredGrid(Grid):
    def __init__(self, rows:int, cols:int):
        super().__init__(rows, cols)
        self._distances = None

    def distances(self, distances):
        print(f"Setting distances {distances}")
        self._distances = distances
        self.farthest, self.max = distances.max

    def _color_of(self, cell):
        distance = self._distances[cell] if cell in self._distances else None

        if not distance:
            return None

        intensity:float = float((self.max - distance)) / self.max
        dark = int((255 * intensity))
        bright = 128 + int(127* intensity)
        return (bright, bright, dark)




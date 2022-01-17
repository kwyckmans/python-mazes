from typing import Optional, Tuple
from core.distances import Distances
from core.grid import Grid
from core.cell import Cell
import math


class ColoredGrid(Grid):
    def __init__(self, rows: int, cols: int):
        super().__init__(rows, cols)
        self.farthest: Optional[Cell] = None
        self.max: int = 0
        self._distances: Optional[Distances] = None

    def distances(self, distances: Distances):
        # print(f"Setting distances {distances}")
        self._distances = distances
        self.farthest, self.max = distances.max

    def _color_of(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        """

        TODO: while what I have works, and can be reused, I can extract the color interpolation and
            make this method easier by having a list or a dict as argument that provides a color
            for each distance. So for max_dist = 10, you'd pass in a list/dict of 10 colors.

            This list can then be generated whichever way you want, for example
            you can interpolate between two colors as described in
            https://gist.github.com/lambdamusic/4734406.

            The important part being that it's decoupled from this method.
        """
        if not self._distances or not cell in self._distances:
            return None

        distance: int = self._distances[cell]

        steps = 4

        # So, If I have 3 steps, red, yellow, green. That means at
        # distance 0 -> color = red = 255, 0, 0
        # distance 5 -> color = yellow = 255, 255, 0
        # distance 10 -> color = green = 0, 255, 0

        # Intensity varies not between 0 and max distance, but between 0 and step.
        # originally : self.max - distance / self.max
        #  10 - 5 / 10 = 0.5 -> Halfway point. Should become 1 now
        # but now, at 0: intensity = 0
        #          at step: intensity = 1
        #          at step + 1: intensity = 0
        # So denonimator becomes (self.max / self. steps)
        #
        # For 2 steps, max = 10 -> denominator = 5
        #     at distance / 2, intensity = 1
        #     at 0: intensity = 0 -> 0/5
        #     at 5: intensity = 1 -> 5/5
        #     at 6: intensity = 0,...
        #     at 10: intensity = 1 -> 5/5
        #
        #  (max - distance) / (max / steps)
        # 10 - 0 / 5 -> 2
        # 10 - 5 / 5 -> 1
        # 10 - 6 / 5 -> 0,8 (should be 0,8...)
        # 10 - 10 / 5 -> 0

        # Let's assume max = 15, steps = 3
        # 15 - 0 / 5 -> 3       | 0 % 3 = 0 |
        # 15 - 1 / 5 -> 2.8     | 1 % 3 = 1 | 1 + 2 * 5
        # 15 - 5 / 5 -> 2       | 5 % 3 = 2 | 5 + 2 * 5
        # 15 - 6 / 5 -> 1.8     | 6 % 3 = 0 | 6 + 1 * 5
        # 15 - 10 /5 -> 1
        # 15 - 11 / 5 -> 0.8    |           | 11 + 0 * 5
        # 15 - 15 /5 -> 0

        # [(max - dist) / (max/steps)] - [max - (max/steps - dist)]
        # or

        interval = int(self.max / steps)
        if interval < 1:
            interval = 1
        # for max 15, interval 3, this gives
        # distance = 0: [5 - (0 - (5 * 0))] / 5 = 5 / 5 = 1
        # distance = 1: [5 - (1 - (5 * 0))] / 5 = 4 / 5 = 0.8
        # distance = 6: [5 - (6 - 5 * ( 6 / 5 ))]  / 5 = [5 - ( 6 - 5) ] / 5 = 4 / 5 = 0.8
        # distance = 14: [ 5 - (14 - 5 * ( 14 / 5))] / 5 = [5 - (14 - 5 * 2)]  = 1 / 5 = 0.2
        intensity = (
            interval - (distance - (interval * math.floor(distance / interval)))
        ) / interval

        step = math.floor(distance / interval)
        # print(
        #     f"max distance: { self.max }, #colors: { steps }, color: {step}, distance: {distance}, intensity: {intensity}"
        # )

        # I know which step I'm in by doing distance / (max / steps):
        # max / steps = 10 / 2 = 5
        # distance 0 -> 0 / 5 = 0th step
        # distance 5 -> 5 / 5 = 1st step
        # distance 10 -> 10 / 5 = 2nd step

        # step: int = int(distance / (self.max / steps))
        # intensity: float = float(((self.max - distance)) / steps) / ((self.max) / steps)

        if 0 <= step < 1:
            # red to yellow
            red = 255
            green = 255 - int(255 * intensity)
            blue = 0
        elif 1 <= step < 2:  #  1 < step <= 2: # I'm at 255, 255, 0 now, need to go to 0, 255, 0
            # yellow to green
            red = int(255 * intensity)
            green = 255
            blue = 0
        elif 2 <= step < 3:
            # green to blue
            red = 0
            green = int(255 * intensity)
            blue = 255 - int(255 * intensity)
        elif 3 <= step < 4:
            # blue to violet
            red = 128 - int(128 * intensity)
            green = 0
            blue = 255
        else:
            # The max distance matches this. Should be violet.
            red = 128
            green = 0
            blue = 255

        # print(f"r: {red}, g: {green}, b: {blue}")
        # assume max = 10
        # Intensity at 0: ((10 - 0) ) / (10/2) = 2
        # Intensity at 5: ((10 - 5) ) / (10/2) = 1
        # Intensity at 10: ((10 - 10)  ) / (10/2) = 0
        # intensity: float = float(((self.max - distance)) / steps) / ((self.max) / steps)

        # Red(255,0,0)
        # Yellow(255,255,0)
        # Green(0,255,0)
        # Blue(0,0,255)
        # Turqoise(0,255,255)
        # Magenta(255,0,255)

        # red = 255  # int(255 * intensity)
        # green = 255 - int(255 * intensity)
        # blue = 0  # 128 + int(127 * intensity)  # 128 + int(127 * intensity)

        # dark = int((255 * intensity))
        # bright = 128 + int(127 * intensity)
        return (red, green, blue)

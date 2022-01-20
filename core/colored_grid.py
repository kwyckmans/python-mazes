from typing import List, Optional, Tuple
from core.distances import Distances
from core.grid import Grid
from core.cell import Cell
import math
from PIL import Image, ImageDraw


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

    def to_gif(self, cell_size: int = 10, line_width: int = 1) -> List[Image.Image]:
        """Returns a list of images that represent a floodfill of the grid. Each image will have incrementally more
        colored boxes, baseed on the distance from origin.

        TODO: A pretty feature would be to not draw the colors in rectangles, but do it in a form of scanline,
           so the floodfill would be smoother, instead of appearing as cubes.

        FIXME: Currently I have to draw the grid every single frame, since if I draw it first, and start from that image
           everytime, the colors will overwrite the grid. The goal is to have it visible in all frames, but draw it only ones.
           The way to achieve this, probably, is to reduce the size of the colored boxes with the size of the grid.
           The tradeoff is that it would run faster, but the code would be more complicated.
        """
        images: List[Image.Image] = []

        img_width = self.nr_cols * cell_size + line_width
        img_height = self.nr_rows * cell_size + line_width

        BACKGROUND = (255, 255, 255)
        WALL = (0, 0, 0)

        # TODO: figure out a cleaner way to do this
        modes = [
            "BACKGROUNDS",
            "WALLS",
        ]  # Currently, the order matters, otehrwise backgrounds will paint over walls

        for i in range(self.max + 1):
            image = Image.new("RGBA", (img_width, img_height), BACKGROUND)
            draw = ImageDraw.Draw(image)
            for mode in modes:
                for cell in self:
                    x1 = cell.col * cell_size
                    y1 = cell.row * cell_size
                    x2 = (cell.col + 1) * cell_size
                    y2 = (cell.row + 1) * cell_size

                    if (
                        mode == "BACKGROUNDS"
                        and self._distances
                        and self._distances[cell] <= i
                    ):
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
            images.append(image)

        return images

    def _color_of(self, cell: Cell) -> Optional[Tuple[int, int, int]]:
        """

        TODO: while what I have works, and can be reused, I can extract the color interpolation and
            make this method easier by having a list or a dict as argument that provides a color
            for each distance. So for max_dist = 10, you'd pass in a list/dict of 10 colors.

            This list can then be generated whichever way you want, for example
            you can interpolate between two colors as described in
            https://gist.github.com/lambdamusic/4734406.

            The important part being that it's decoupled from this method.

            Alternatively, I could have a dict with colors, representing the gradient. So, in the
            case of the rainbow, you'd have something like:
                colors: {
                    0: RED
                    1: YELLOW
                    2: GREEN
                    3: BLUE
                    4: VIOLET
                }

            I could then get the color with
                interval = int(self.max / steps) # max distance is split up in a number of intervals
                steps = len(colors) - 1 # we count the changes, not the number of colors
                current_step = math.floor(distance / interval)
                color = colors[current_step]

            and then adjust that color based on intensity that I'd still calculate in this method,
            based on distance.
        """
        if not self._distances or not cell in self._distances:
            return None

        distance: int = self._distances[cell]

        steps = 4

        interval = int(self.max / steps)
        if interval < 1:
            interval = 1

        intensity = (
            interval - (distance - (interval * math.floor(distance / interval)))
        ) / interval

        step = math.floor(distance / interval)
        # print(
        #     f"max distance: { self.max }, #colors: { steps }, color: {step}, distance: {distance}, intensity: {intensity}"
        # )

        if step == 0:
            # red to yellow
            red = 255
            green = 255 - int(255 * intensity)
            blue = 0
        elif (
            step == 1
        ):  #  1 < step <= 2: # I'm at 255, 255, 0 now, need to go to 0, 255, 0
            # yellow to green
            red = int(255 * intensity)
            green = 255
            blue = 0
        elif step == 2:
            # green to blue
            red = 0
            green = int(255 * intensity)
            blue = 255 - int(255 * intensity)
        elif step == 3:
            # blue to violet
            red = 128 - int(128 * intensity)
            green = 0
            blue = 255
        else:
            # The max distance matches this. Should be violet.
            red = 128
            green = 0
            blue = 255
            print(
                f"max distance: { self.max }, #colors: { steps }, color: {step}, distance: {distance}, intensity: {intensity}"
            )

        # print(f"r: {red}, g: {green}, b: {blue}")
        return (red, green, blue)

from random import randrange, choice
from core.grid import Grid


class Sidewinder:
    @staticmethod
    def on(grid: Grid):
        for row in grid.cells:
            run = []

            for cell in row:
                run.append(cell)

                at_eastern_boundary = cell.east == None
                at_northern_boundary = cell.north == None

                should_close_out = at_eastern_boundary or (
                    not at_northern_boundary and randrange(2) == 0
                )

                if should_close_out:
                    member = choice(run)
                    if member.north:
                        member.link(member.north)
                    run.clear()
                else:
                    cell.link(cell.east)

        return grid

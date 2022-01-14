from random import randrange, choice
from typing import List
from core.cell import Cell
from core.grid import Grid


class Sidewinder:
    @staticmethod
    def on(grid: Grid):
        for row in grid.cells:
            run: List[Cell] = []

            for _, cell in grid.cells[row].items():
                run.append(cell)

                at_eastern_boundary = cell.east is None
                at_northern_boundary = cell.north is None

                should_close_out = at_eastern_boundary or (
                    not at_northern_boundary and randrange(2) == 0
                )

                if should_close_out:
                    member = choice(run)
                    if member.north:
                        member.link_biderectional(member.north)
                    run.clear()
                else:
                    if cell.east:
                        cell.link_biderectional(cell.east)

        return grid

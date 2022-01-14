from core.grid import Grid


def test_creating_grid_sets_up_a_2d_grid():
    grid = Grid(2, 2)
    cell = grid[1][1]

    assert cell is not None


def test_creating_grid_assigns_cell_neighbours():
    grid = Grid(2, 2)
    cell = grid[1][1]
    north_cell = cell.north

    assert north_cell
    assert north_cell.row == 0
    assert north_cell.col == 1

    east_cell = cell.east

    assert not east_cell

    south_cell = cell.south

    assert not south_cell

    west_cell = cell.west

    assert west_cell
    assert west_cell.row == 1
    assert west_cell.col == 0


def test_iterating_over_grid_goes_column_first():
    grid = Grid(2, 2)
    cells = [cell for cell in grid]

    assert len(cells) == 4
    assert cells[1].row == 0 and cells[1].col == 1

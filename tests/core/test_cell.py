from core.cell import Cell


def test_new_cell_has_no_neighbours():
    cell = Cell(0, 0)
    assert cell.north is None
    assert cell.south is None
    assert cell.east is None
    assert cell.west is None


def test_new_cell_has_no_links():
    cell = Cell(0, 0)

    assert len(cell.links) == 0


def test_link_cell_links_cell():
    cell_A = Cell(0, 0)
    cell_B = Cell(1, 1)

    cell_A.link(cell_B)

    assert cell_A.is_linked(cell_B)
    assert not cell_B.is_linked(cell_A)


def test_link_cells_bidirectional_links_both_cells():
    cell_A = Cell(0, 0)
    cell_B = Cell(1, 1)

    cell_A.link_biderectional(cell_B)

    assert cell_A.is_linked(cell_B)
    assert cell_B.is_linked(cell_A)


def test_unlink_cells_unlinks_cell():
    cell_A = Cell(0, 0)
    cell_B = Cell(1, 1)

    cell_A.link_biderectional(cell_B)
    cell_A.unlink(cell_B)

    assert not cell_A.is_linked(cell_B)
    assert cell_B.is_linked(cell_A)


def test_unlink_cells_bidirectional_unlinks_both_cells():
    cell_A = Cell(0, 0)
    cell_B = Cell(1, 1)

    cell_A.link_biderectional(cell_B)
    cell_A.unlink_bidirectional(cell_B)

    assert not cell_A.is_linked(cell_B)
    assert not cell_B.is_linked(cell_A)


def test_neighbours_empty_when_no_neighbours():
    cell_A = Cell(0, 0)
    neigbours = cell_A.neighbors()
    assert len(neigbours) == 0


def test_neighbours_contains_cell_if_neighbour():
    cell_A = Cell(0, 0)
    cell_B = Cell(1, 1)

    cell_A.north = cell_B

    neigbours = cell_A.neighbors()
    assert cell_B in neigbours


def test_get_links_empty_when_no_links():
    cell_A = Cell(0, 0)
    links = cell_A.links
    assert len(links) == 0


def test_get_links_contains_cell_when_linked():
    cell_A = Cell(0, 0)
    cell_B = Cell(1, 1)

    cell_A.link(cell_B)
    links = cell_A.links
    assert cell_B in links

# backend/tests/test_cell.py
import pytest
from ..game.cell import Cell

class TestCellState:
    @pytest.mark.parametrize("x, y", [
        (0, 0), (0, 1), (1, 0),
        (-1, -1), (-1, 0), (0, -1),
        (-1, 1), (1, -1)
    ])

    def test_initial_state(self, x, y):
        cell = Cell(x, y)
        assert cell.x == x
        assert cell.y == y
        assert not cell.is_mine
        assert not cell.is_revealed
        assert not cell.is_flagged
        assert cell.neighbor_mines == 0

    def test_place_mine(self):
        cell = Cell(0, 0)
        cell.place_mine()
        assert cell.is_mine is True
        cell.place_mine()
        assert cell.is_mine is True

    def test_reveal_safe(self):
        cell = Cell(0, 0)
        cell.reveal()
        assert cell.is_revealed is True
        cell.reveal()
        assert cell.is_revealed is True

    def test_reveal_mine(self):
        cell = Cell(0, 0)
        cell.place_mine()
        cell.reveal()
        assert cell.is_revealed is True
        cell.reveal()
        assert cell.is_revealed is True

    def test_reveal_flagged(self):
        cell = Cell(0, 0)
        cell.toggle_flagged()
        cell.reveal()
        assert cell.is_revealed is False

    def test_toggle_flag(self):
        cell = Cell(0, 0)
        assert cell.is_flagged is False
        cell.toggle_flagged()
        assert cell.is_flagged is True
        cell.toggle_flagged()
        assert cell.is_flagged is False

    def test_neighbor_mines_assignment(self):
        cell = Cell(0, 0)
        cell.neighbor_mines = 5
        assert cell.neighbor_mines == 5
        cell.neighbor_mines = -1
        assert cell.neighbor_mines == -1

    def test_to_dict(self):
        cell = Cell(0, 0)
        dictionary = cell.to_dict()
        assert isinstance(dictionary, dict)
        assert dictionary["x"] == cell.x
        assert dictionary["y"] == cell.y
        assert dictionary["is_flagged"] == cell.is_flagged
        assert dictionary["is_revealed"] == cell.is_revealed
        assert dictionary["is_mine"] == cell.is_mine
        assert dictionary["neighbor_mines"] == cell.neighbor_mines

class TestCellString:
    def test_str_unrevealed(self):
        cell = Cell(0, 0)
        assert str(cell) == "."

    def test_str_flagged(self):
        cell = Cell(0, 0)
        cell.toggle_flagged()
        assert str(cell) == "F"

    def test_str_revealed_mine(self):
        cell = Cell(0, 0)
        cell.place_mine()
        cell.reveal()
        assert str(cell) == "*"

    @pytest.mark.parametrize("neighbor_count, expected", [
        (0, "0"),
        (1, "1"),
        (5, "5"),
        (97, "97"),
        (-1, "-1"),
    ])

    def test_str_revealed(self, neighbor_count, expected):
        cell = Cell(0, 0)
        cell.neighbor_mines = neighbor_count
        cell.reveal()
        assert str(cell) == expected
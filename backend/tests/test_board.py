# test/tests/test_board.py

import re
import pytest
from ..game.board import Board
from ..exceptions import InvalidMoveError, InvalidConfigurationError

class TestBoardState:
    @pytest.mark.parametrize("width, height", [
    (1, 1), (10, 10)
    ])
    def test_valid_initial_state(self, width, height):        
        board = Board(width, height)
        assert board.width == width
        assert board.height == height
        for x in range(width):
            for y in range(height):
                cell = board.get_cell(x, y)
                assert cell.x == x
                assert cell.y == y

        bottom_left = board.get_cell(0, 0)
        assert bottom_left.x == 0
        assert bottom_left.y == 0
        assert bottom_left.neighbor_mines == 0
        assert not bottom_left.is_mine
        assert not bottom_left.is_revealed

        top_right = board.get_cell(width - 1, height - 1)
        assert top_right.x == width - 1
        assert top_right.y == height - 1
        assert top_right.neighbor_mines == 0
        assert not top_right.is_mine
        assert not top_right.is_revealed

        assert board.get_cell(-1, 0) is None
        assert board.get_cell(0, -1) is None
        assert board.get_cell(width, 0) is None
        assert board.get_cell(0, height) is None
        assert board.get_cell(width, height) is None

    @pytest.mark.parametrize("width, height", [
    (-1, -1), (-1, 1), (1, -1),
    (0, 1), (1, 0), (0, 0),
    (-1, 0), (0, -1)
    ])
    def test_invalid_dimensions(self, width, height):
        with pytest.raises(InvalidConfigurationError, match=re.escape("Width and height must be positive.")):
                board = Board(width, height)

    def test_place_mine_at(self):
        board = Board(1, 1)

        assert board.place_mine_at(0, 0)
        assert not board.place_mine_at(0, 0)
        # No need for a list, this depends on place_mine, tested on "test_cell"
        assert not board.place_mine_at(-1, -1)

    def test_get_neighbors(self):
        board = Board(3, 3)

        assert len(board.get_neighbors(1, 1)) == 8
        assert len(board.get_neighbors(0, 0)) == 3
        assert len(board.get_neighbors(0, 1)) == 5
        assert len(board.get_neighbors(-1, -1)) == 1 # (0, 0)
        assert len(board.get_neighbors(-2, -2)) == 0

    def test_flag(self):
        board = Board(2, 2)

        board.flag(0, 0)
        assert board.get_cell(0, 0).is_flagged
        
        board.reveal_cell(1, 1)
        with pytest.raises(InvalidMoveError, match=re.escape("Cell (-1, -1) is out of bounds.")):
            board.flag(-1, -1)

        with pytest.raises(InvalidMoveError, match=re.escape("Cell (1, 1) is already revealed.")):
            board.flag(1, 1)

    def test_get_neighbor_mine_count(self):
        board = Board(3, 3)

        cell = board.get_cell(1, 1)
        assert cell.neighbor_mines == 0

        i = 1
        for neighbor in board.get_neighbors(1, 1):
            board.place_mine_at(neighbor.x, neighbor.y)
            cell = board.get_cell(1, 1)
            assert cell.neighbor_mines == i
            i += 1

    def test_reveal_cell(self):
        board = Board(3, 3)
        board.place_mine_at(2, 2) # corner
        board.flag(1, 2) # to test recursiveness

        assert not board.reveal_cell(1, 1)
        safe_cell = board.get_cell(1, 1) # do i need this? is this a pointer?
        assert safe_cell.is_revealed
        assert str(safe_cell) == "1"

        for neighbor in board.get_neighbors(safe_cell.x, safe_cell.y):
            assert not neighbor.is_revealed # because the revealed cell has a neighboring mine

        assert not board.reveal_cell(0, 0) # No neighbor mines, no kaboom
        # verify recursiveness for the left side and bottom (both have no neighbor mines)
        assert board.get_cell(0, 1).is_revealed
        assert board.get_cell(1, 0).is_revealed
        assert board.get_cell(2, 0).is_revealed
        # this one has a neighbor mine, but its neighbor doesnt
        # it also has no flag and itself isnt a mine
        # recursiveness should reveal this cell
        assert board.get_cell(2, 1).is_revealed

        flagged_cell = board.get_cell(1, 2)
        assert not flagged_cell.is_revealed

        mine_cell = board.get_cell(2, 2)
        assert not mine_cell.is_revealed

        assert board.reveal_cell(2, 2)
        mine_cell = board.get_cell(2, 2)
        assert mine_cell.is_revealed

    def test_invalid_reveal_cell (self):
        board = Board(2, 2)
        board.flag(1, 1)
        board.reveal_cell(0, 0)

        with pytest.raises(InvalidMoveError, match=re.escape("Cell (-1, -1) is out of bounds.")):
            board.reveal_cell(-1, -1)

        with pytest.raises(InvalidMoveError, match=re.escape("Cell (0, 0) is already revealed.")):
            board.reveal_cell(0, 0)

        with pytest.raises(InvalidMoveError, match=re.escape("Cell (1, 1) is flagged.")):
            board.reveal_cell(1, 1)

    def test_to_str(self):
        board = Board(3, 3)

        board.place_mine_at(2, 2)
        board.flag(2, 1)
        board.reveal_cell(1, 1)
        board.reveal_cell(2, 2)

        # left to right, up to down.
        # x++ until \n, then x = 0.
        # y = height, y-- at \n.
        assert str(board) == "| . | . | * |\n| . | 1 | F |\n| . | . | . |"

    def test_to_dict(self):
        board = Board(2, 2)

        board_list = board.to_dict()
        
        assert isinstance(board_list, list)

        assert len(board_list) == board.height
        for y, row in enumerate(board_list):
            assert len(row) == board.width
            for x, cell in enumerate(row):
                assert isinstance(cell, dict)
                assert cell["x"] == board.get_cell(x, y).x
                assert cell["y"] == board.get_cell(x, y).y
                assert cell["is_flagged"] == board.get_cell(x, y).is_flagged
                assert cell["is_revealed"] == board.get_cell(x, y).is_revealed
                assert cell["is_mine"] == board.get_cell(x, y).is_mine
                assert cell["neighbor_mines"] == board.get_cell(x, y).neighbor_mines
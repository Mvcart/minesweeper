# tests/test_game.py

import re
import pytest
from ..game.game import Game
from ..game.gamestate import GameState
from ..exceptions import InvalidConfigurationError, GameAlreadyEndedError

class TestGameState:
    def test_valid_initial_state(self, seeded_game_42):
        game = seeded_game_42

        assert game.state == GameState.PLAYING

        assert game.board.get_cell(2, 2).is_revealed
        assert not game.board.get_cell(2, 2).is_mine
        for neighbor in game.board.get_neighbors(2, 2):
            assert neighbor.is_revealed
            assert not neighbor.is_mine

        n_mines = 0
        for y in range(5):
            for x in range(5):
                if game.board.get_cell(x, y).is_mine:
                    n_mines += 1
        
        assert n_mines == 3

    def test_loose_condition(self, seeded_game_42):
        lost_game = seeded_game_42

        lost_game.click(4,0)
        assert lost_game.board.get_cell(4, 0).is_mine
        assert lost_game.state == GameState.LOST

    def test_win_condition(self, seeded_game_42):
        won_game = seeded_game_42

        assert not won_game.board.get_cell(0, 2).is_mine
        assert not won_game.board.get_cell(0, 1).is_mine
        assert not won_game.board.get_cell(0, 4).is_mine
        won_game.click(0, 2)
        won_game.click(0, 1)
        won_game.click(0, 4)
        assert won_game.state == GameState.WON

    def test_flag(self, seeded_game_42):
        game = seeded_game_42

        assert not game.board.get_cell(0, 2).is_revealed
        game.flag(0, 2)
        assert game.board.get_cell(0, 2).is_flagged
    
    def test_negative_mine_count(self):
        with pytest.raises(InvalidConfigurationError, match=re.escape("Mine count cannot be negative.")):
            Game(1, 1, -2, 0, 0, seed=42)
        
    def test_invalid_first_click(self):
        with pytest.raises(InvalidConfigurationError, match=re.escape("Invalid first click coordinates.")):
            Game(5, 5, 2, -1, 0, seed=42)
    
    def test_too_may_mines(self):
        with pytest.raises(InvalidConfigurationError, match=re.escape("Too many mines for this board size. Max mines: 16")):
            Game(5, 5, 25, 2, 2, seed=42)

    def test_click_after_game_over(self, seeded_game_42):
        with pytest.raises(GameAlreadyEndedError, match=re.escape("Game is already lost.")):
            lost_game = seeded_game_42

            lost_game.click(4,0)
            assert lost_game.board.get_cell(4, 0).is_mine
            assert lost_game.state == GameState.LOST

            lost_game.click(2, 2)

    def test_flag_after_game_over(self, seeded_game_42):
        with pytest.raises(GameAlreadyEndedError, match=re.escape("Game is already lost.")):
            lost_game = seeded_game_42

            lost_game.click(4,0)
            assert lost_game.board.get_cell(4, 0).is_mine
            assert lost_game.state == GameState.LOST

            lost_game.flag(4, 0)

    def test_to_dict_lost(self, seeded_game_42):
        lost_game = seeded_game_42

        dictionary = lost_game.to_dict()

        assert isinstance(dictionary, dict)
        assert dictionary["id"] == lost_game.id
        assert dictionary["state"] == lost_game.state.value
        assert dictionary["width"] == lost_game.width
        assert dictionary["height"] == lost_game.height
        assert dictionary["mine_count"] == lost_game.mine_count
        assert dictionary["start_time"] == lost_game.start_time.isoformat()
        assert dictionary["end_time"] == None
        assert len(dictionary["board"]) == lost_game.height
        for row in dictionary["board"]:
            assert len(row) == lost_game.width

        for y in range(lost_game.height):
            for x in range(lost_game.width):
                if lost_game.board.get_cell(x, y).is_revealed:
                    assert dictionary["board"][y][x]["is_mine"] == lost_game.board.get_cell(x, y).is_mine
                    assert dictionary["board"][y][x]["neighbor_mines"] == lost_game.board.get_cell(x, y).neighbor_mines
                else:
                    assert dictionary["board"][y][x]["is_mine"] == False
                    assert dictionary["board"][y][x]["neighbor_mines"] == None

        lost_game.click(4,0)
        dictionary = lost_game.to_dict()
        
        assert dictionary["state"] == lost_game.state.value
        assert dictionary["end_time"] == lost_game.end_time.isoformat()
        for y in range(lost_game.height):
            for x in range(lost_game.width):
                assert dictionary["board"][y][x]["is_mine"] == lost_game.board.get_cell(x, y).is_mine
                assert dictionary["board"][y][x]["neighbor_mines"] == lost_game.board.get_cell(x, y).neighbor_mines

    def test_to_dict_won(self, seeded_game_42):
        won_game = seeded_game_42

        dictionary = won_game.to_dict()

        assert isinstance(dictionary, dict)
        assert dictionary["id"] == won_game.id
        assert dictionary["state"] == won_game.state.value
        assert dictionary["width"] == won_game.width
        assert dictionary["height"] == won_game.height
        assert dictionary["mine_count"] == won_game.mine_count
        assert dictionary["start_time"] == won_game.start_time.isoformat()
        assert dictionary["end_time"] == None
        assert len(dictionary["board"]) == won_game.height
        for row in dictionary["board"]:
            assert len(row) == won_game.width

        for y in range(won_game.height):
            for x in range(won_game.width):
                if won_game.board.get_cell(x, y).is_revealed:
                    assert dictionary["board"][y][x]["is_mine"] == won_game.board.get_cell(x, y).is_mine
                    assert dictionary["board"][y][x]["neighbor_mines"] == won_game.board.get_cell(x, y).neighbor_mines
                else:
                    assert dictionary["board"][y][x]["is_mine"] == False
                    assert dictionary["board"][y][x]["neighbor_mines"] == None

        won_game.click(0, 2)
        won_game.click(0, 1)
        won_game.click(0, 4)
        dictionary = won_game.to_dict()
        
        assert dictionary["state"] == won_game.state.value
        assert dictionary["end_time"] == won_game.end_time.isoformat()
        for y in range(won_game.height):
            for x in range(won_game.width):
                assert dictionary["board"][y][x]["is_mine"] == won_game.board.get_cell(x, y).is_mine
                assert dictionary["board"][y][x]["neighbor_mines"] == won_game.board.get_cell(x, y).neighbor_mines
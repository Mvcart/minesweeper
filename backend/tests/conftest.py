# tests/conftest.py

import pytest
from ..game.game import Game

"""
    Seeded game (all revealed):
    Game(5, 5, 3, 2, 2, seed=42) =
    | 1 | 1 | 0 | 0 | 0 |
    | * | 1 | 0 | 0 | 0 |
    | 1 | 1 | 0 | 0 | 0 |
    | 1 | 1 | 0 | 1 | 1 |
    | * | 1 | 0 | 1 | * |
"""
@pytest.fixture
def seeded_game_42_waiting() -> Game:
    return Game(
        width=5,
        height=5,
        mine_count=3,
        seed=42)

@pytest.fixture
def first_click_coordinates_seeded_game_42() -> dict:
    return {
        "x": 2,
        "y": 2
        }

@pytest.fixture
def seeded_game_42_playing(
    first_click_coordinates_seeded_game_42,
    seeded_game_42_waiting
    ) -> Game:
    game = seeded_game_42_waiting
    game.start(
        first_click_x = first_click_coordinates_seeded_game_42["x"],
        first_click_y = first_click_coordinates_seeded_game_42["y"]
        )
    return game
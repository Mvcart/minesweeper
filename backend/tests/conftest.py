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
def seeded_game_42() -> Game:
    return Game(5, 5, 3, 2, 2, seed=42)
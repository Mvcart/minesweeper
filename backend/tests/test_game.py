# backend/tests/test_game.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # For finding the "game" dir

from game.game import Game

game = Game(5, 5, 2, 2, 2)
print(f"Seed: {game.seed}")
print(f"Placement Strategy: {type(game.placement_strategy)}")
print(f"{game.board}")
print()
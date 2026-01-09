# backend/tests/test_board_logic.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # For finding the "game" dir

from game.board import Board

board = Board(5,5)
print(board)
board.place_mine_at(2, 1)
board.place_mine_at(2, 2)
board.place_mine_at(2, 4)
print(f"")
print(board)
board.reveal_cell(0,0)
print(f"")
print(board)
board.reveal_cell(4,0)
print(f"")
print(board)
board.reveal_cell(2, 0)
print(f"")
print(board)
board.place_mine_at(2, 3)
print(f"")
print(board)
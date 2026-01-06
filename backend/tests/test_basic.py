# backend/tests/test_basic.py

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))) # For finding the "game" dir

from game.cell import Cell
from game.board import Board

b = Board(8,6)
print(f'Board: {b.width}x{b.height}')
print(f'Cell (0,0): {b.grid[0][0]}')
b.grid[0][0].reveal()
print(f'Revealed (0,0): {b.grid[0][0]}')
print(f'Number of neighbors of (3,3): {len(b.get_neighbors(3, 3))}')
print(f'Neighbors of (3,3):')
for neighbor in b.get_neighbors(3, 3):
    print(f'({neighbor.x}, {neighbor.y}): {neighbor}')
b.grid[2][2].place_mine()
b.grid[2][2].toggle_flagged()
b.grid[2][2].reveal()
b.grid[2][3].place_mine()
b.grid[2][3].reveal()
b.grid[2][4].place_mine()
print(f'Updated neighbors of (3,3):')
for neighbor in b.get_neighbors(3, 3):
    print(f'({neighbor.x}, {neighbor.y}): {neighbor}')
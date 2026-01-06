# backend/game/board.py

from typing import List, Optional
from .cell import Cell

class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y)
                      for y in range(height)] 
                      for x in range(width)]
        
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def get_neighbors(self, x: int, y: int) -> List[Cell]:
        neighbors: List[Cell] = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                cell = self.get_cell(x + dx, y + dy)
                if cell:
                    neighbors.append(cell)
        return neighbors
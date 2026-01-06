# backend/game/board.py

from typing import List, Optional
from .cell import Cell

"""
    Basic board class for minesweeper
    Orchestrates the "Cell" object

    Future: Make dynamic board a possibility, making the neighbor mine count dynamic.
"""

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
                neighbor_cell = self.get_cell(x + dx, y + dy)
                if neighbor_cell:
                    neighbors.append(neighbor_cell)
        return neighbors

    def reveal_cell(self, x: int, y: int) -> bool:
        # Cell does not exist, dumbo
        if self.get_cell(x, y) is None:
            print("This shouldnt happen, invalid cell")
            return False

        # Kaboom
        if self.grid[x][y].is_mine:
            return True

        # Recursive logic
        if self.neighbor_mine_count(x, y) == 0:
            self.reveal_cell_recursive(x, y)
        else:
            self.grid[x][y].reveal()

        # No kaboom
        return False

    # lazy neighbor mine count (change to dynamic for different game modes!)
    def neighbor_mine_count(self, x: int, y: int) -> int:
        cell = self.grid[x][y]

        if cell._neighbor_mines is not None:
            return cell.neighbor_mines

        neighbor_mines = 0
        for neighbor in self.get_neighbors(x, y):
            if neighbor.is_mine:
                neighbor_mines += 1
        return neighbor_mines
    
    # Recursive cell revealing logic
    def reveal_cell_recursive(self, x: int, y: int) -> None:
        current_cell = self.grid[x][y]
        
        current_cell.reveal()

        if self.neighbor_mine_count(x, y) == 0:
            for neighbor in self.get_neighbors(x, y):
                # Reveal neighbor
                if not neighbor.is_revealed:
                    neighbor.reveal()
                
                    # If this neighbor has 0 adjacent mines, reveal their neighbors
                    if self.neighbor_mine_count(neighbor.x, neighbor.y) == 0:
                        self.reveal_cell_recursive(neighbor.x, neighbor.y)

    def calculate_all_neighbors(self) -> None:
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                if not cell.is_mine:
                    count = self.neighbor_mine_count(x, y)
                    cell.set_neighbor_mines(count)

    def __str__(self) -> str:
        rows = []
        for y in reversed(range(self.height)):
            row_cells = [str(self.grid[x][y]) for x in range(self.width)]
            rows.append("| " + " | ".join(row_cells) + " |")
        return "\n".join(rows)


    # FIX CACHE DEFINING
    def place_mine_at(self, x: int, y: int) -> None:
        cell = self.get_cell(x, y)
        if cell:
            cell.place_mine()
            # Clean neighbor cache
            for nx, ny in [(x+dx, y+dy) for dx in (-1,0,1) for dy in (-1,0,1) if not (dx==0 and dy==0)]:
                neighbor = self.get_cell(nx, ny)
                if neighbor:
                    neighbor._neighbor_mines = None
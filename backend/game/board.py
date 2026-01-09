# backend/game/board.py

from typing import List, Optional, Tuple, Dict
from .cell import Cell

"""
    Basic board class for minesweeper
    Orchestrates the "Cell" object

    Future: Make dynamic board a possibility, making the neighbor mine count dynamic.
"""

NEIGHBOR_OFFSETS = {(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)}

class Board:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y)
                      for y in range(height)] 
                      for x in range(width)]
        self._neighbor_cache: Dict[Tuple[int, int], int] = {} # (x, y) -> count

    def reveal_cell(self, x: int, y: int) -> bool:
        # Cell does not exist, dumbo
        cell_to_reveal = self.get_cell(x, y)
        if cell_to_reveal is None:
            print("This shouldnt happen, invalid cell")
            return False

        # Cell is already revealed, duh
        if cell_to_reveal.is_revealed:
            print("This shouldn't happen, this is already revealed")
            return False

        # Kaboom
        if cell_to_reveal.is_mine:
            return True

        # Recursive logic
        if self.get_neighbor_mine_count(x, y) == 0:
            self._reveal_cell_recursive(x, y)
        else:
            cell_to_reveal.reveal()

        # No kaboom
        return False

    # mine placement logic
    def place_mine_at(self, x: int, y: int) -> bool:
        cell = self.get_cell(x, y)
        if not cell or cell.is_mine:
            return False

        cell.place_mine()

        # Invalidate cache for all affected cells
        self._invalidate_cache_for_cell_and_neighbors(x, y)
        
        # Recalculate neighbor counts for all affected cells
        self._update_neighbor_counts_for_cell_and_neighbors(x, y)

        return True

    # lazy neighbor mine count (change to dynamic for different game modes!)
    def get_neighbor_mine_count(self, x: int, y: int) -> int:
        cache_key = (x, y)
        
        if cache_key in self._neighbor_cache:
            return self._neighbor_cache[cache_key]
        
        n_neighboring_mines = self._count_neighboring_mines(x, y)
        self._neighbor_cache[cache_key] = n_neighboring_mines

        cell = self.get_cell(x, y)
        if cell:
            cell.neighbor_mines = n_neighboring_mines
        return n_neighboring_mines
        
    def get_neighbors(self, x: int, y: int) -> List[Cell]:
        neighbors: List[Cell] = []
        for offset_x, offset_y in NEIGHBOR_OFFSETS:
            neighbor_cell = self.get_cell(x + offset_x, y + offset_y)
            
            if neighbor_cell:
                neighbors.append(neighbor_cell)
        return neighbors
        
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    # Private methods:
    
    # Recursive cell revealing logic
    def _reveal_cell_recursive(self, x: int, y: int) -> None:
        current_cell = self.grid[x][y]
        
        current_cell.reveal()

        if self.get_neighbor_mine_count(x, y) != 0:
            return

        for neighbor in self.get_neighbors(x, y):
            # If neighbor is not revealed yet...
            if neighbor.is_revealed:
                continue
            
            # ...Reveal it!
            neighbor.reveal()
        
            # If this neighbor has 0 adjacent mines, also reveal its neighbors
            if self.get_neighbor_mine_count(neighbor.x, neighbor.y) == 0:
                self._reveal_cell_recursive(neighbor.x, neighbor.y)
    
    def _invalidate_cache_for_cell_and_neighbors(self, x: int, y: int) -> None:
        self._neighbor_cache.pop((x, y), None)
        
        for neighbor in self.get_neighbors(x, y):
            self._neighbor_cache.pop((neighbor.x, neighbor.y), None)

    def _update_neighbor_counts_for_cell_and_neighbors(self, x: int, y:int) -> None:
        if not self._cell_exists(x, y):
            return
    
        self.get_neighbor_mine_count(x, y)

        for neighbor in self.get_neighbors(x, y):
            self.get_neighbor_mine_count(neighbor.x, neighbor.y)

    def _count_neighboring_mines(self, x: int, y: int) -> int:
        neighbor_mines = 0
        
        for neighbor in self.get_neighbors(x, y):
            if neighbor.is_mine:
                neighbor_mines += 1
        
        return neighbor_mines
    
    def _cell_exists(self, x: int, y:int) -> bool:
        cell = self.get_cell(x, y)
        if not cell:
            return False
        
        return True

    def __str__(self) -> str:
        rows = []
        for y in reversed(range(self.height)):
            row_cells = [str(self.grid[x][y]) for x in range(self.width)]
            rows.append("| " + " | ".join(row_cells) + " |")
        return "\n".join(rows)
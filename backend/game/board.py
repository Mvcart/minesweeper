# backend/game/board.py

from typing import List, Optional, Tuple, Dict

from backend.exceptions import InvalidMoveError, InvalidConfigurationError
from .cell import Cell

"""
    Basic board class for minesweeper
    Orchestrates the f"Cell" object

    Future: Make dynamic board a possibility, making the neighbor mine count dynamic.
            Make convex board shapes work (it doesnt seem very difficult)
"""

NEIGHBOR_OFFSETS = {(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)}

class Board:
    """
    Minesweeper grid.
    Manages cells, mine placement, neighbor queries and reveal logic.
    """
    def __init__(self, width: int, height: int) -> None:
        if width <= 0 or height <= 0:
            raise InvalidConfigurationError("Width and height must be positive.")

        self.width = width
        self.height = height
        self.grid = [[
            Cell(x, y)
            for y in range(height)] 
            for x in range(width)]
        self._neighbor_cache: Dict[Tuple[int, int], int] = {} # (x, y) -> count

    # flag on/off switch
    def flag(self, x: int, y: int) -> None:
        cell = self._get_cell_or_raise(x, y)

        if cell.is_revealed:
            return

        cell.toggle_flagged()

    # reveal cell logic (can trigger recursive logic)
    def reveal_cell(self, x: int, y: int) -> bool:
        # Cell does not exist
        cell_to_reveal = self._get_cell_or_raise(x, y)

        # Cell is already revealed
        if cell_to_reveal.is_revealed:
            neighbors = self.get_neighbors(x, y)
            flag_count = 0
            for neighbor in neighbors:
                if neighbor.is_flagged:
                    flag_count += 1

            if flag_count == cell_to_reveal.neighbor_mines:
                for neighbor in neighbors:
                    if not neighbor.is_revealed and not neighbor.is_flagged:
                        self.reveal_cell(neighbor.x, neighbor.y)
            return

        # Cell is flagged
        if cell_to_reveal.is_flagged:
            return

        # Kaboom
        if cell_to_reveal.is_mine:
            cell_to_reveal.reveal()
            return True

        cell_to_reveal.reveal()

        # Recursive logic
        if self.get_neighbor_mine_count(x, y) == 0:
            self._reveal_cell_recursive(x, y)

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
    
    # returns the list of neighbors
    def get_neighbors(self, x: int, y: int) -> List[Cell]:
        neighbors: List[Cell] = []
        for offset_x, offset_y in NEIGHBOR_OFFSETS:
            neighbor_cell = self.get_cell(x + offset_x, y + offset_y)
            
            if neighbor_cell:
                neighbors.append(neighbor_cell)
        return neighbors
        
    # returns the Cell object
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def to_dict(self) -> dict:
        board_list = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(self.get_cell(x, y).to_dict())
            board_list.append(row)
        return board_list

    # Private methods:
    # Recursive cell revealing logic (reveal only safe cells)
    def _reveal_cell_recursive(self, x: int, y: int) -> None:
        if self.get_neighbor_mine_count(x, y) != 0:
            return

        for neighbor in self.get_neighbors(x, y):
            # If neighbor is not revealed (or flagged) yet...
            if neighbor.is_revealed or neighbor.is_flagged:
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

    def _get_cell_or_raise(self, x: int, y: int) -> Cell:
        cell = self.get_cell(x, y)
        if cell is None:
            raise InvalidMoveError(f"Cell ({x}, {y}) is out of bounds.")
        return cell

    def __str__(self) -> str:
        rows = []
        for y in reversed(range(self.height)):
            row_cells = [str(self.grid[x][y]) for x in range(self.width)]
            rows.append("| " + " | ".join(row_cells) + " |")
        return "\n".join(rows)
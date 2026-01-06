# backend/game/cell.py

from typing import Optional

class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self._neighbor_mines: Optional[int] = None  # Cache

    def place_mine(self) -> None:
        self.is_mine = True

    def reveal(self) -> None:
        if not self.is_flagged:
            self.is_revealed = True

    def toggle_flagged(self) -> None:
        self.is_flagged = not self.is_flagged

    @property
    def neighbor_mines(self) -> int:
        if self._neighbor_mines is None:
            return 0
        return self._neighbor_mines
    
    def set_neighbor_mines(self, count: int) -> None:
        self._neighbor_mines = count
    
    def __str__(self) -> str:
        if self.is_flagged:
            return "F"
        if not self.is_revealed:
            return "."
        if self.is_mine:
            return "*"
        return str(self.neighbor_mines)
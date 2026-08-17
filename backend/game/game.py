# backend/game/game.py

import secrets
from datetime import datetime
from typing import Optional, List, Tuple

from .board import Board
from .gamestate import GameState
from backend.strategies.mine_placement import MinePlacementStrategy, RandomMinePlacement
from backend.exceptions import GameAlreadyEndedError, InvalidMoveError, InvalidConfigurationError

class Game:
    # Public methods
    def __init__(self, 
                 width: int, 
                 height: int, 
                 mine_count: int, 
                 first_click_x: int, 
                 first_click_y: int,
                #  safe_zone_strategy_class: Optional[SafeZoneStrategy] = None, # TO IMPLEMENT IN THE FUTURE
                 placement_strategy_class: Optional[MinePlacementStrategy] = None,
                 seed: Optional[int] = None,
                 ) -> None:
        if mine_count < 0:
            raise InvalidConfigurationError("Mine count cannot be negative.")
        # The first click cant be a mine
        if not self._valid_first_click(width, height, first_click_x, first_click_y):
            raise InvalidConfigurationError("Invalid first click coordinates.")
        
        if seed is None:
            seed = secrets.randbits(64)

        self.seed = seed
        
        self.width = width
        self.height = height
        self.board = Board(width, height)
        self.mine_count = mine_count
        safe_cells = self._get_safe_zone(first_click_x, first_click_y)

        max_mines = (width * height) - len(safe_cells)
        if mine_count > max_mines:
            raise InvalidConfigurationError(f"Too many mines for this board size. Max mines: {(max_mines)}")

        # self.safe_zone_strategy = safe_zone_strategy

        if placement_strategy_class is None:
            placement_strategy_class = RandomMinePlacement
            
        self.placement_strategy = placement_strategy_class(seed = self.seed)

        mine_positions = self.placement_strategy.place_mines(
            width,
            height,
            mine_count,
            safe_cells,)
        
        for x, y in mine_positions:
            self.board.place_mine_at(x, y)
        
        self.board.reveal_cell(first_click_x, first_click_y)

        self.state = GameState.PLAYING
        self.start_time: Optional[datetime] = datetime.now()
        self.end_time: Optional[datetime] = None

    # Click/reveal func. updates game state
    def click(self, x: int, y: int) -> None:
        if self.state != GameState.PLAYING:
            raise GameAlreadyEndedError(f"Game is already {self.state.value}.")
        
        hit_mine = self.board.reveal_cell(x, y)

        if hit_mine:
            self.state = GameState.LOST
            self.end_time = datetime.now()
        elif self._check_win():
            self.state = GameState.WON
            self.end_time = datetime.now()

    # Toggle flag
    def flag(self, x: int, y: int) -> None:
        if self.state != GameState.PLAYING:
            raise GameAlreadyEndedError(f"Game is already {self.state.value}.")

        self.board.flag(x, y)
    
    # Private methods
    # Maybe outsource this func like the mine placement?
    def _get_safe_zone(self, x: int, y: int) -> List[Tuple[int, int]]:
        safe_zone = []
        center = self.board.get_cell(x, y)
        safe_zone.append((center.x, center.y))

        for neighbor in self.board.get_neighbors(x, y):
            safe_zone.append((neighbor.x, neighbor.y))

        return safe_zone

    def _valid_first_click(self, width: int, height: int, x: int, y: int) -> bool:
        if x < 0 or x >= width:
            return False
        
        if y < 0 or y >= height:
            return False
        
        return True

    def _check_win(self):
        # walks thorough each cell verifying if every safe cell is revealed
        for x in range(self.width):
            for y in range(self.height):
                cell = self.board.get_cell(x, y)
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def __str__(self) -> str:
        return str(self.board);
# backend/game/game.py

import secrets
import uuid
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
                #  safe_zone_strategy_class: Optional[SafeZoneStrategy] = None, # TO IMPLEMENT IN THE FUTURE
                 placement_strategy_class: Optional[MinePlacementStrategy] = None,
                 seed: Optional[int] = None,
                 ) -> None:
        if mine_count < 0:
            raise InvalidConfigurationError("Mine count cannot be negative.")
        
        if seed is None:
            seed = secrets.randbits(64)

        self.seed = seed
        
        self.width = width
        self.height = height
        self.board = Board(width, height)
        self.mine_count = mine_count

        self.id = str(uuid.uuid4())

        # self.safe_zone_strategy = safe_zone_strategy

        if placement_strategy_class is None:
            placement_strategy_class = RandomMinePlacement
            
        self.placement_strategy = placement_strategy_class(seed = self.seed)

        self.state = GameState.WAITING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def start(self, first_click_x: int, first_click_y: int) -> None:
        # The first click can't be outside the board
        if not self._valid_first_click(first_click_x, first_click_y):
            raise InvalidConfigurationError("Invalid first click coordinates.")
            
        safe_cells = self._get_safe_zone(first_click_x, first_click_y)
        max_mines = (self.width * self.height) - len(safe_cells)
        if self.mine_count > max_mines:
            raise InvalidConfigurationError(f"Too many mines for this board size. Max mines: {(max_mines)}")

        mine_positions = self.placement_strategy.place_mines(
            self.width,
            self.height,
            self.mine_count,
            safe_cells)
        
        for x, y in mine_positions:
            self.board.place_mine_at(x, y)
        
        self.state = GameState.PLAYING

        self.click(first_click_x, first_click_y)
        self.start_time = datetime.now()

    # Click/reveal func. updates game state
    def click(self, x: int, y: int) -> None:
        if self.state == GameState.WAITING:
            self.start(x, y)
        elif self.state != GameState.PLAYING:
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

    def to_dict(self) -> dict:
        data = {}
        data["id"] = self.id
        data["state"] = self.state.value
        data["width"] = self.width
        data["height"] = self.height
        data["mine_count"] = self.mine_count
        data["start_time"] = self.start_time.isoformat() if self.start_time else None
        data["end_time"] = self.end_time.isoformat() if self.end_time else None
        data["board"] = self.board.to_dict()
        if self.state == GameState.PLAYING or self.state == GameState.WAITING:
            for line in data["board"]:
                for cell in line:
                    if not cell["is_revealed"]:
                        cell["is_mine"] = False
                        cell["neighbor_mines"] = None

        return data

    @staticmethod
    def get_absolute_max_mines(width: int, height: int) -> int:
        # worst-case scenario
        return (width * height) - 1

    # Private methods
    # Maybe outsource this func like the mine placement?
    def _get_safe_zone(self, x: int, y: int) -> List[Tuple[int, int]]:
        safe_zone = []
        center = self.board.get_cell(x, y)
        safe_zone.append((center.x, center.y))

        for neighbor in self.board.get_neighbors(x, y):
            safe_zone.append((neighbor.x, neighbor.y))

        return safe_zone

    def _valid_first_click(self, x: int, y: int) -> bool:
        if x < 0 or x >= self.width:
            return False
        
        if y < 0 or y >= self.height:
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
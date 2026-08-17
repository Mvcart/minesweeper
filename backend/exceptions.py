# backend/exceptions.py

__all__ = [
    "MinesweeperError",
    "InvalidConfigurationError",
    "InvalidMoveError",
    "GameAlreadyEndedError"
]

class MinesweeperError(Exception):
    """Base exception for all minesweeper errors."""
    pass

class InvalidConfigurationError(MinesweeperError):
    """Raised when game parameters are invalid (e.g., mine_count > cells)."""
    pass

class InvalidMoveError(MinesweeperError):
    """Raised when a move cannot be performed (out of bounds, already revealed, flagged, etc.)."""
    pass

class GameAlreadyEndedError(MinesweeperError):
    """Raised when trying to interact with a finished game."""
    pass
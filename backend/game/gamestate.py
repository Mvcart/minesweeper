# backend/game/gamestate.py

from enum import Enum

class GameState(Enum):
    PLAYING = "playing"
    WAITING = "waiting for first click"
    WON = "won"
    LOST = "lost"
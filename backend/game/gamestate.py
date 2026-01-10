# backend/game/gamestate.py

from enum import Enum

class GameState(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"
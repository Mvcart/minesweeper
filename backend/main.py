from backend.game.game import Game
from backend.exceptions import *

from typing import Dict
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
    )

games = {}

def handle_game_error(e: Exception):
    if isinstance(e, (InvalidConfigurationError, InvalidMoveError)):
        return {"error": str(e)}, 400
    if isinstance(e, GameAlreadyEndedError):
        return {"error": str(e)}, 409
    return {"error": str(e)}, 500

@app.post("/game")
async def create_game(params: Dict):
    try:
        game = Game(
            width=params["width"],
            height=params["height"],
            mine_count=params["mine_count"],
            )

        games[game.id] = game

        return game.to_dict()
    except Exception as e:
        return handle_game_error(e)

@app.post("/game/{game_id}/click")
async def click(game_id: str, params: Dict):
    game = games.get(game_id)

    if not game:
        return {"error": "game not found"}, 404

    try:
        game.click(params["x"], params["y"])
    except Exception as e:
        return handle_game_error(e)

    return game.to_dict()

@app.post("/game/{game_id}/flag")
async def flag(game_id: str, params: Dict):
    game = games.get(game_id)

    if not game:
        return {"error": "game not found"}, 404

    try:
        game.flag(params["x"], params["y"])
    except Exception as e:
        return handle_game_error(e)

    return game.to_dict()

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
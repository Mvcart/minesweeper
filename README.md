# Minesweeper

Full-stack Minesweeper game with Python backend and web interface.

## Features

- Classic Minesweeper gameplay
- First-click safe guarantee
- Flagging and recursive reveal
- REST API with FastAPI
- Clean web interface

## Technologies

- Backend: Python, FastAPI
- Frontend: Vanilla JS, CSS Grid
- Testing: pytest

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn backend.main:app --reload
```

## Open browser at `http://localhost:8000`

## Project Structure

```lua
minesweeper/
├── backend
│   ├── exceptions.py   # custom exceptions
│   ├── game            # game classes
│   ├── main.py         # FastAPI startup
│   ├── strategies      # mine placement/safe zone strategies
│   └── tests           # pytest tests
└── frontend            # basic frontend files
    ├── index.html
    ├── script.js
    └── style.css
```

## LICENSE

[MIT](LICENSE)

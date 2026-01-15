# Minesweeper Game Engine

A clean, well-architected Minesweeper game engine in Python, showcasing object-oriented design, testability, and extensibility.

## Status

**Core engine complete** - Backend game logic is functional and ready for frontend integration.

## Features

- Clean OOP architecture with strategy pattern
- Seed-based reproducibility for testing
- Extensible mine placement algorithms
- Recursive cell revealing logic

## Quick Start

```bash
git clone https://github.com/yourusername/minesweeper.git
cd minesweeper/backend
python -m tests.test_game
```

## Architecture

Clean separation between:

- Cell: Individual cell state
- Board: Grid management and reveal logic
- Game: Game orchestration and rules
- MinePlacementStrategy: Pluggable mine algorithms

## Project Structure

```
backend/
├── game/          # Core game logic
├── strategies/    # Mine placement algorithms
└── tests/         # Test suite
```

## Usage Example

Run from the `backend/` directory:

```python

from game.game import Game

game = Game(width=9, height=9, mine_count=10, 
            first_click_x=4, first_click_y=4, seed=42)
print(game.board)
```

## License

MIT License
# backend/strategies/mine_placement.py

from abc import ABC, abstractmethod
from typing import List, Tuple
import random

class MinePlacementStrategy(ABC):
    @abstractmethod
    def place_mines(self,
                    width: int,
                    height: int,
                    mine_count: int,
                    forbidden_cells: List[Tuple[int, int]],
                    seed: int,
                    ) -> List[Tuple[int, int]]:
        pass

"""
    NOTE: This method doesnt guarantees that a game is winnable. Example:
    Game(5,5,3,2,2,seed=42) =
    | . | 1 | 0 | 0 | 0 |
    | . | 1 | 0 | 0 | 0 |
    | . | 1 | 0 | 0 | 0 |
    | . | 1 | 0 | 1 | 1 |
    | . | 1 | 0 | 1 | . |

    Notice that there is no way to guarantee where are the two mines at the left side.
    FUTURE: Make a strategy that guarantees that the placement is winnable 
"""
class RandomMinePlacement(MinePlacementStrategy):
    def __init__(self, seed: int):
        self.seed = seed

    def place_mines(self, width, height, mine_count, forbidden_cells):
        all_cells = [(x, y) for x in range(width) for y in range(height)]

        available_cells = [cell for cell in all_cells if cell not in forbidden_cells]
        
        if mine_count > len(available_cells):
            raise ValueError(f"Cannot place {mine_count} mines in {len(available_cells)} available cells")

        rng = random.Random(self.seed)
        return rng.sample(list(available_cells), mine_count)
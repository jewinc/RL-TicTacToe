import numpy as np
from move import MoveType


class Agent:
    def __init__(self, seed=42):
        np.random.seed(seed)

    def move(self):
        """
        return a random move
        """
        i = np.random.randint(low=0, high=len(MoveType.all_moves()), size=1)
        return list(MoveType.all_moves())[i[0]]

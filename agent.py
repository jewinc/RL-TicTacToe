import numpy as np
from global_var import MOVES

class Agent:
    def __init__(self, seed=42):
        np.random.seed(seed)

    def move(self):
        '''
        return a random move
        '''
        i = np.random.randint(low=0, high=len(MOVES.keys()), size=1)
        return list(MOVES.keys())[i[0]]
        
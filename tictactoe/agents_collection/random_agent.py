import random

from tictactoe.agent import Agent


class RandomAgent(Agent):
    def __init__(self, symbol):
        super().__init__(symbol)
        random.seed()

    def choose_move(self, board):
        """
        Return a random move from the list of valid moves.
        """
        return random.choice(self.get_valid_moves(board))

import random

from tictactoe.agent import Agent, AgentType
from tictactoe.move import MoveType


class RandomAgent(Agent):
    def __init__(self, symbol):
        super().__init__(AgentType.RANDOM, symbol)
        random.seed()

    def choose_move(self, board) -> MoveType:
        """
        Return a random move from the list of valid moves.
        """
        return random.choice(self.get_valid_moves(board))

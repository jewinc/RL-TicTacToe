import random

from tictactoe.agent import Agent, AgentType
from tictactoe.move import MoveType


class RandomAgent(Agent):
    def __init__(self):
        super().__init__(AgentType.RANDOM)
        random.seed()

    def choose_move(self, board) -> MoveType:
        """
        Return a random move from the list of valid moves.
        """
        return random.choice(self.get_valid_moves(board))
    
    def __str__(self):
        return f"{self.agent_type}"

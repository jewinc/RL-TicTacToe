from abc import abstractmethod
from enum import Enum
import logging

from tictactoe.player import Player, PlayerType, Symbol
from tictactoe.move import MoveType


class AgentType(Enum):
    RANDOM = 0
    MINIMAX = 1
    REINFORCEMENT = 2


class Agent(Player):
    def __init__(self, agent_type: AgentType):
        super().__init__(PlayerType.AGENT)
        self.agent_type = agent_type

    def get_valid_moves(self, board):
        valid_moves = [
            move
            for move in MoveType.all_moves()
            if board.is_full() is False and board.is_move_valid(move)
        ]

        if not valid_moves:
            logging.error("No valid moves available for the random player.")
            return None

        return valid_moves

    @abstractmethod
    def choose_move(self, board):
        pass

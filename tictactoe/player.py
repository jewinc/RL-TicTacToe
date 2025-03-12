from abc import abstractmethod
from enum import Enum

from tictactoe.move import MoveType
from tictactoe.board import Symbol


class PlayerType(Enum):
    HUMAN = 0
    AGENT = 1

    def __str__(self):
        return f"{self.name}"


class Player:
    def __init__(self, player_type: PlayerType):
        self._player_type = player_type
        self._symbol = None

    @property
    def player_type(self):
        return self._player_type

    @property
    def symbol(self):
        if self._symbol is None:
            raise ValueError("Player symbol is not set.")
        return self._symbol
    
    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @abstractmethod
    def choose_move(self, board):
        pass
    
    def reset(self):
        pass


class HumanPlayer(Player):
    def __init__(self, name=str):
        super().__init__(PlayerType.HUMAN)
        
        self.name = name

    def choose_move(self, board):
        while True:
            player_input = input("Choose your move (e.g. HG, MM, BD): ")
            move = MoveType.from_str(player_input)
            if move is None:
                print("Invalid move. Please try again.")
            elif not board.is_move_valid(move):
                print("Move already played or invalid, try another one.")
            else:
                return move
    
    def __str__(self) -> str:
        return self.name

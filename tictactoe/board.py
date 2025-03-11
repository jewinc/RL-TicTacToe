from enum import Enum
from typing import List, Tuple

from tictactoe.move import MoveType


class Symbol(Enum):
    X = "X"
    O = "O"
    EMPTY = "."

    def __str__(self):
        return f"{self.value}"


BoardType = List[List[Symbol]]
Coordinates = Tuple[int, int]


class Board:
    def __init__(self):
        self.board: BoardType = [[Symbol.EMPTY for _ in range(3)] for _ in range(3)]

    def __str__(self) -> str:
        row_sep = "-------"
        board_string = f"{row_sep}\n"
        for row in self.board:
            board_string += "|".join([""] + [str(cell) for cell in row] + [""]) + "\n"
            board_string += f"{row_sep}\n"
        return board_string

    def get_board(self) -> BoardType:
        return self.board

    def get(self, move: MoveType) -> Symbol:
        return self.board[move.row][move.col]

    def set_move(self, move: MoveType, symbol: Symbol):
        self.board[move.row][move.col] = symbol

    def reset(self):
        self.board = [[Symbol.EMPTY for _ in range(3)] for _ in range(3)]

    def has_winner(self) -> Tuple[bool, Symbol]:
        """
        Win conditions are:
        - 3 X or O in one row (e.g [X, X, X])
        or in one column (e.g [X, X, X])
        or in diagonal (e.g
        [O, , ] or [ , ,X]
        [ ,O, ]    [ ,X, ]
        [ , ,O]    [X, , ])

        Returns:
        - bool: True if there is a winner, False otherwise
        - Player: the winner if there is one, None otherwise
        """
        # Check rows and columns
        for i in range(3):
            if (
                self.board[i][0] == self.board[i][1] == self.board[i][2]
                and self.board[i][0] != Symbol.EMPTY
            ):
                return True, self.board[i][0]
            if (
                self.board[0][i] == self.board[1][i] == self.board[2][i]
                and self.board[0][i] != Symbol.EMPTY
            ):
                return True, self.board[0][i]

        # Check diagonals
        if self.board[1][1] != Symbol.EMPTY and (
            (self.board[0][0] == self.board[1][1] == self.board[2][2])
            or (self.board[0][2] == self.board[1][1] == self.board[2][0])
        ):
            return True, self.board[1][1]

        return False, Symbol.EMPTY

    def is_full(self) -> bool:
        """
        Check if the board is full.
        Returns:
        - bool: True if the board is full, False otherwise
        """
        return all(cell != Symbol.EMPTY for row in self.board for cell in row)

    def is_draw(self) -> bool:
        """
        Check if the game is in draw.
        The game is in draw if there is no winner and the board is full.
        Returns:
        - bool: True if the game is in draw, False otherwise
        """
        win, _ = self.has_winner()
        return not win and self.is_full()

    def is_move_valid(self, move: MoveType) -> bool:
        """
        Check if the move is valid.
        A move is valid if the cell is empty.
        Args:
        - move: MoveType
        Returns:
        - bool: True if the move is valid, False otherwise
        """
        return move in MoveType.all_moves() and self.get(move) == Symbol.EMPTY

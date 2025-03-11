import pytest

from tictactoe.board import Board, Symbol
from tictactoe.move import MoveType


@pytest.fixture
def board():
    """Fixture to provide a fresh board instance for each test."""
    return Board()


@pytest.mark.parametrize("move", MoveType.all_moves())
@pytest.mark.parametrize("symbol", [Symbol.X, Symbol.O])
def test_play_move(board, move, symbol):
    """Test that playing any move changes the board state.
    and that the board state changes to the expected value."""
    state0 = board.get(move)
    board.set_move(move, symbol)
    state1 = board.get(move)
    assert state0 != state1, "Board state did not change after playing a move."
    assert (
        state1 == symbol
    ), "Board state did not change to the expected value after playing a move."


@pytest.mark.parametrize("row", [MoveType.H_row(), MoveType.M_row(), MoveType.B_row()])
@pytest.mark.parametrize("symbol", [Symbol.X, Symbol.O])
def test_rows_win(board, row, symbol):
    """Test that winning conditions for rows are detected."""
    for move in row:
        board.set_move(move, symbol)
    won, _ = board.has_winner()
    assert won, "Winning condition for rows not detected."


@pytest.mark.parametrize("col", [MoveType.G_col(), MoveType.M_col(), MoveType.D_col()])
@pytest.mark.parametrize("symbol", [Symbol.X, Symbol.O])
def test_cols_win(board, col, symbol):
    """Test that winning conditions for columns are detected."""
    for move in col:
        board.set_move(move, symbol)
    won, _ = board.has_winner()
    assert won, "Winning condition for columns not detected."


@pytest.mark.parametrize(
    "moves",
    [
        MoveType.H_diag(),
        MoveType.D_diag(),
    ],
)
@pytest.mark.parametrize("symbol", [Symbol.X, Symbol.O])
def test_diagonals_win(board, moves, symbol):
    """Test that winning conditions for diagonals are detected."""
    for move in moves:
        board.set_move(move, symbol)
    won, _ = board.has_winner()
    assert won, "Winning condition for diagonals not detected."

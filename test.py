import pytest

from board import Board
from move import MoveType


@pytest.fixture
def board():
    """Fixture to provide a fresh board instance for each test."""
    return Board()


@pytest.mark.parametrize("move", MoveType.all_moves())
@pytest.mark.parametrize("player", [True, False])
def test_play_move(board, move, player):
    """Test that playing any move changes the board state.
    and that the board state changes to the expected value."""
    state0 = board.get(move)
    board.play(move, player)
    state1 = board.get(move)
    assert state0 != state1, "Board state did not change after playing a move."
    assert (
        state1 == player
    ), "Board state did not change to the expected value after playing a move."


@pytest.mark.parametrize("row", [MoveType.H_row(), MoveType.M_row(), MoveType.B_row()])
@pytest.mark.parametrize("player", [True, False])
def test_rows_win(board, row, player):
    """Test that winning conditions for rows are detected."""
    for move in row:
        board.play(move, player)
    assert board.win()[0]


@pytest.mark.parametrize("col", [MoveType.G_col(), MoveType.M_col(), MoveType.D_col()])
@pytest.mark.parametrize("player", [True, False])
def test_cols_win(board, col, player):
    """Test that winning conditions for columns are detected."""
    for move in col:
        board.play(move, player)
    assert board.win()[0]


@pytest.mark.parametrize(
    "moves",
    [
        MoveType.H_diag(),
        MoveType.D_diag(),
    ],
)
@pytest.mark.parametrize("player", [True, False])
def test_diagonals_win(board, moves, player):
    """Test that winning conditions for diagonals are detected."""
    for move in moves:
        board.play(move, player)
    assert board.win()[0]

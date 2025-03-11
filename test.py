import pytest

from board import Board
from global_var import MOVES

@pytest.fixture
def board():
    """Fixture to provide a fresh board instance for each test."""
    return Board()

@pytest.mark.parametrize("move", ["HG", "HM", "HD", "MG", "MM", "MD", "BG", "BM", "BD"])
@pytest.mark.parametrize("player", [True, False])
def test_play_move(board, move, player):
    """Test that playing any move changes the board state.
    and that the board state changes to the expected value."""
    state0 = board.get(move)
    board.play(move, player)
    state1 = board.get(move)
    assert state0 != state1, "Board state did not change after playing a move."
    assert state1 == player, "Board state did not change to the expected value after playing a move."

@pytest.mark.parametrize("row", ["H", "M", "B"])
@pytest.mark.parametrize("player", [True, False])
def test_rows_win(board, row, player):
    """Test that winning conditions for rows are detected."""
    board.play(f"{row}G", player)
    board.play(f"{row}M", player)
    board.play(f"{row}D", player)
    assert board.win()[0]

@pytest.mark.parametrize("col", ["G", "M", "D"])
@pytest.mark.parametrize("player", [True, False])
def test_cols_win(board, col, player):
    """Test that winning conditions for columns are detected."""
    board.play(f"H{col}", player)
    board.play(f"M{col}", player)
    board.play(f"B{col}", player)
    assert board.win()[0]

@pytest.mark.parametrize("moves", [
    ["HG", "MM", "BD"],  # First diagonal win
    ["HD", "MM", "BG"]   # Second diagonal win
])
@pytest.mark.parametrize("player", [True, False])
def test_diagonals_win(board, moves, player):
    """Test that winning conditions for diagonals are detected."""
    for move in moves:
        board.play(move, bool(player))
    assert board.win()[0]
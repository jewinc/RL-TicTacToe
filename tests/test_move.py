import pytest

from tictactoe.move import MoveType


def test_move_row():
    """Test that the row property of the HD move is 0."""
    move = MoveType.HD
    assert move.row == 0, "Row property of HD move is not 0."


def test_move_col():
    """Test that the column property of the HD move is 2."""
    move = MoveType.HD
    assert move.col == 2, "Column property of HD move is not 2."


def test_print_move():
    """Test that the string representation of HG move is 'HG'."""
    move = MoveType.HG
    assert str(move) == "HG"


def test_from_str():
    """Test that the move string 'MM' is converted to the MM move."""
    move_str = "MM"
    move = MoveType.from_str(move_str)
    assert move == MoveType.MM

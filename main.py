from board import Board
from test import Test 

def main():
    board = Board()
    print(str(board))

    Test.run()

    board.start()

main()
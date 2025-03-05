from board import Board, MOVES
from test import Test 
from agent import Agent

def main():
    board = Board()
    #print(str(board))

    Test.run()

    board.start()
    
main()
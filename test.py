from board import Board, MOVES

class Test:
    
    def play_move():
        board = Board()
        state0 = board.get('HG')
        board.play('HG', False)
        assert(state0!=board.get('HG'))

        for move in MOVES.keys():
            state_before = board.get(move)
            board.play(move, True)
            assert(state_before!=board.get(move))

    
    def rows_win():
        board1 = Board()
        player:int = 1
        board1.play("HG", bool(player))
        board1.play("HM", bool(player))
        board1.play("HD", bool(player))
        assert(board1.win()[0]==True)
        
        board2 = Board()
        board2.play("MG", bool(player))
        board2.play("MM", bool(player))
        board2.play("MD", bool(player))
        assert(board2.win()[0]==True)
        
        board3 = Board()
        board3.play("BG", bool(player))
        board3.play("BM", bool(player))
        board3.play("BD", bool(player))
        assert(board3.win()[0]==True)
        
    def cols_win():
        board1 = Board()
        player:int = 1
        board1.play("HG", bool(player))
        board1.play("MG", bool(player))
        board1.play("BG", bool(player))
        assert(board1.win()[0]==True)
        
        board2 = Board()
        board2.play("HM", bool(player))
        board2.play("MM", bool(player))
        board2.play("BM", bool(player))
        assert(board2.win()[0]==True)
        
        board3 = Board()
        board3.play("HD", bool(player))
        board3.play("MD", bool(player))
        board3.play("BD", bool(player))
        assert(board3.win()[0]==True)

    def diagonals_win():
        board1 = Board()
        player:int = 1
        board1.play("HG", bool(player))
        board1.play("MM", bool(player))
        board1.play("BD", bool(player))
        assert(board1.win()[0]==True)
        
        board2 = Board()
        board2.play("HD", bool(player))
        board2.play("MM", bool(player))
        board2.play("BG", bool(player))
        assert(board2.win()[0]==True)

    @staticmethod
    def run():
        Test.play_move()
        Test.rows_win()
        Test.cols_win()
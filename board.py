MOVES: dict[str, tuple[int]] = {
        'HG': (0,0),
        'HM': (0,1),
        'HD': (0,2),
        'MG': (1,0),
        'MM': (1,1),
        'MD': (1,2),
        'BG': (2,0),
        'BM': (2,1),
        'BD': (2,2)
}



class Board:
    def __init__(self):
        self.board: list[list[bool]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
    
    def __str__(self):

        def print_move(move:bool):
            """
            Param: boolean move
            Return: corresponding rendering
            """
            if move:
                return 'X'
            else:
                return 'O'
        
        row_str: bool = "-------"
        board_string = f"{row_str}\n"
        for row in self.board:
            board_string += "|"
            for move in row:
                move_str = print_move(move)
                board_string+= f"{move_str}|"
            board_string+= f"\n{row_str}\n"

        return board_string
    
    def win(self)->bool:
        """
        Win conditions are:
        - 3 X or O in one row (e.g [X, X, X])
          or in one column (e.g [X, 
                                 X, 
                                 X]
        )
        or in diagonal (e.g 
        [O, , ]     [ , ,X]
        [ ,O, ]     [ ,X, ]
        [ , ,O]     [X, , ]
        )
        Return: return true if there is a winner
        """
        winner: int = -1
        for i in range(3):
            row_win: bool = (self.board[i][0]==self.board[i][1]==self.board[i][2]) and isinstance(self.board[i][0], bool)
            col_win: bool = ((self.board[0][i]==self.board[1][i]==self.board[2][i])) and isinstance(self.board[0][i], bool)
            if row_win:
                winner = int(self.board[i][0])
            elif col_win:
                winner = int(self.board[0][i])
        diag_win: bool = ((self.board[0][0]==self.board[1][1]==self.board[2][2]) or (self.board[2][0]==self.board[1][1]==self.board[0][2])) and isinstance(self.board[1][1], bool)
        if diag_win:
            winner = int(self.board[1][1])
        return winner > 0
    
    def draw(self):
        """
        The game is in draw if all the move has been played and there is not a winner
        Return: return is the game is draw by checking board completion and if there is a winner
        """
        if self.win():
            return False
        else:
            for i in range(3):
                for j in range(3):
                    if not(isinstance(self.board[i][j], bool)):
                        print("\nThere is still move to play !\n")
                        return False
            return True

    def play(self, move:str, player:bool):
        coords:tuple[int] = MOVES[move]
        self.board[coords[0]][coords[1]] =  player


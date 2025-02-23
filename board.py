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


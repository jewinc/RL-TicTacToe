from agent import Agent
from move import MoveType


class Board:
    def __init__(self):
        self.board: list[list[bool]] = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]

    def __str__(self):

        def print_move(move: bool):
            """
            Param: boolean move
            Return: corresponding rendering
            """
            if not (isinstance(move, bool)):
                return "E"
            elif move:
                return "X"
            else:
                return "O"

        row_str: bool = "-------"
        board_string = f"{row_str}\n"
        for row in self.board:
            board_string += "|"
            for move in row:
                move_str = print_move(move)
                board_string += f"{move_str}|"
            board_string += f"\n{row_str}\n"

        return board_string

    def win(self) -> tuple[bool, int]:
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
            row_win: bool = (
                self.board[i][0] == self.board[i][1] == self.board[i][2]
            ) and isinstance(self.board[i][0], bool)
            col_win: bool = (
                (self.board[0][i] == self.board[1][i] == self.board[2][i])
            ) and isinstance(self.board[0][i], bool)
            if row_win:
                winner = int(self.board[i][0])
            elif col_win:
                winner = int(self.board[0][i])
        diag_win: bool = (
            (self.board[0][0] == self.board[1][1] == self.board[2][2])
            or (self.board[2][0] == self.board[1][1] == self.board[0][2])
        ) and isinstance(self.board[1][1], bool)
        if diag_win:
            winner = int(self.board[1][1])
        return (winner >= 0, winner)

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
                    if not (isinstance(self.board[i][j], bool)):
                        print("\nThere is still move to play !\n")
                        return False
            return True

    def play(self, move: MoveType, player: bool):
        coords: tuple[int] = move.value
        self.board[coords[0]][coords[1]] = player

    def get(self, move: MoveType) -> bool:
        coords: tuple[int] = move.value
        return self.board[coords[0]][coords[1]]

    def check_move_valid(self, move: MoveType) -> bool:
        return not (isinstance(self.get(move), bool)) and (move in MoveType.all_moves())

    def start(self):
        def move_choice(board: Board) -> str:
            player_move_str: str = input("Choose a move : ")
            player_move: MoveType = MoveType.from_str(player_move_str)
            while not player_move or not (board.check_move_valid(player_move)):
                if not player_move:
                    player_move_str = input("Invalid move, choose another one : ")
                else:
                    player_move_str: str = input(
                        "Move already played, choose another one : "
                    )
                player_move: MoveType = MoveType.from_str(player_move_str)
            return player_move

        def ai_move_choice(agents: list[Agent], nb_ai: int, turn: bool) -> str:
            if nb_ai == 2:
                return agents[int(turn)].move()
            elif nb_ai == 1:
                return agents[0].move()

        ongoing: bool = True
        turn: bool = False
        nb_players: int = int(input("Choose the number of players: "))

        while nb_players not in [0, 1, 2]:
            nb_players: int = int(input("Invalid number of players, choose 1 or 2: "))

        # Agents init depending of nb of players
        agents: list[object] = []
        for i in range(2 - nb_players):
            agents.append(Agent(i * 42))

        # Running a game until a win or all move played
        while ongoing:
            print(f"{self}Player's {int(turn) + 1} turn")
            if (nb_players == 2) or (nb_players == 1 and not (turn)):
                move = move_choice(self)
            else:
                move = ai_move_choice(agents=agents, nb_ai=len(agents), turn=turn)
                while not (self.check_move_valid(move)):
                    move = ai_move_choice(agents=agents, nb_ai=len(agents), turn=turn)

            self.play(move, turn)  # Play move on board
            turn = not (turn)  # Turn change

            # Check if game is ended
            winner = self.win()
            if winner[0]:
                ongoing = False
                print(self)
                print(f"The winner is player {winner[1]+1} !")
            elif self.draw():
                ongoing = False

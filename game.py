from tictactoe.agent import AgentType
from tictactoe.board import Board
from tictactoe.player_manager import PlayerManager


class Game:
    def __init__(self):
        self.board = Board()
        self.player_manager = PlayerManager(
            agentA_type=None,
            agentB_type=AgentType.RANDOM,
        )

    def start(self):
        # Running a game until a win or all moves played
        while True:
            player = self.player_manager.current_player
            print(f"Player {player.symbol} turn:")
            move = player.choose_move(self.board)
            self.board.set_move(move, player.symbol)
            print(self.board)

            is_won, winner = self.board.has_winner()
            if is_won:
                print(f"Player {winner} wins!")
                break

            if self.board.is_full():
                print("It's a draw!")
                break
            self.player_manager.switch_player()


if __name__ == "__main__":
    game = Game()
    game.start()

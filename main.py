from enum import Enum

from config import Config

from tictactoe.board import Board
from tictactoe.player import Player, PlayerType
from tictactoe.player_manager import PlayerManager

class Game:
    class Winner(Enum):
        DRAW = "draw"
        PLAYER_A = "playerA"
        PLAYER_B = "playerB"

    def __init__(self, board: Board, playerA: Player, playerB: Player):
        self.board = board
        self.playerA = playerA
        self.playerB = playerB
        self.player_manager = PlayerManager(playerA, playerB)
        
        if playerA.player_type == PlayerType.HUMAN or playerB.player_type == PlayerType.HUMAN:
            self.show_board = True
        else:
            self.show_board = False

    def play(self) -> Winner:
        """
        Play a game between two players.
        Returns:
            EndGame: The result of the game from the perspective of the first player.
        """
        # Running a game until a win or all moves played
        while True:
            player = self.player_manager.current_player
            print(f"{player} turn (symbol: {player.symbol}):") if self.show_board else None
            
            move = player.choose_move(self.board)
            self.board.set_move(move, player.symbol)
            
            print(self.board) if self.show_board else None

            is_won, winner_symbol = self.board.has_winner()
            if is_won:
                winner = self.player_manager.get_player_from_symbol(winner_symbol)
                print(f"{winner} won!") if self.show_board else None
                return Game.Winner.PLAYER_A if winner == self.playerA else Game.Winner.PLAYER_B

            if self.board.is_full():
                print("It's a draw!") if self.show_board else None
                return Game.Winner.DRAW
            self.player_manager.switch_player()


if __name__ == "__main__":
    game = Game(Board(), Config.PLAYER_A, Config.PLAYER_B)
    
    stats = {
        Game.Winner.DRAW: 0,
        Game.Winner.PLAYER_A: 0,
        Game.Winner.PLAYER_B: 0,
    }
    
    for _ in range(Config.NUM_GAMES):
        result = game.play()
        stats[result] += 1
        game.board.reset()
        game.player_manager.reset()
        
    
    print("Game stats:")
    print(f"{str(Config.PLAYER_A)} vs {str(Config.PLAYER_B)}")
    print(f"Number of games: {Config.NUM_GAMES}")
    print(f"Draw: {stats[Game.Winner.DRAW]}")
    print(f"{str(Config.PLAYER_A)} wins: {stats[Game.Winner.PLAYER_A]}")
    print(f"{str(Config.PLAYER_B)} wins: {stats[Game.Winner.PLAYER_B]}")

from enum import Enum

from tictactoe.board import Board
from tictactoe.player import Player, PlayerType
from tictactoe.player_manager import PlayerManager

from tictactoe.player import HumanPlayer
from tictactoe.agents_collection.random_agent import RandomAgent
from tictactoe.agents_collection.reinforcement_agent import ReinforcementAgent, ModelDifficulty

# Defining players
HUMAN_ONE = HumanPlayer(name="Player A")
HUMAN_TWO = HumanPlayer(name="Player B")
RANDOM_AGENT = RandomAgent()
REINFORCEMENT_AGENT_EASY = ReinforcementAgent(model_difficulty=ModelDifficulty.EASY)
REINFORCEMENT_AGENT_MEDIUM = ReinforcementAgent(model_difficulty=ModelDifficulty.MEDIUM)
REINFORCEMENT_AGENT_HARD = ReinforcementAgent(model_difficulty=ModelDifficulty.HARD)

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
    board = Board()
    playerA = HUMAN_ONE
    playerB = REINFORCEMENT_AGENT_HARD
    
    game = Game(board, playerA, playerB)
    
    if playerA.player_type == PlayerType.HUMAN or playerB.player_type == PlayerType.HUMAN:
        NUM_GAMES = 1
    else:
        NUM_GAMES = 10000
    
    stats = {
        Game.Winner.DRAW: 0,
        Game.Winner.PLAYER_A: 0,
        Game.Winner.PLAYER_B: 0,
    }
    
    for _ in range(NUM_GAMES):
        result = game.play()
        stats[result] += 1
        game.board.reset()
        game.player_manager.reset()
        
    
    print("Game stats:")
    print(f"{str(playerA)} vs {str(playerB)}")
    print(f"Number of games: {NUM_GAMES}")
    print(f"Draw: {stats[Game.Winner.DRAW]}")
    print(f"{str(playerA)} wins: {stats[Game.Winner.PLAYER_A]}")
    print(f"{str(playerB)} wins: {stats[Game.Winner.PLAYER_B]}")

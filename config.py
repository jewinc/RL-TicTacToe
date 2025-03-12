from dataclasses import dataclass

from tictactoe.player import Player, HumanPlayer

from tictactoe.agents_collection.random_agent import RandomAgent
from tictactoe.agents_collection.reinforcement_agent import ReinforcementAgent, ModelDifficulty

HUMAN_ONE = HumanPlayer(name="Player A")
HUMAN_TWO = HumanPlayer(name="Player B")
RANDOM_AGENT = RandomAgent()
REINFORCEMENT_AGENT_EASY = ReinforcementAgent(model_difficulty=ModelDifficulty.EASY)
REINFORCEMENT_AGENT_MEDIUM = ReinforcementAgent(model_difficulty=ModelDifficulty.MEDIUM)
REINFORCEMENT_AGENT_HARD = ReinforcementAgent(model_difficulty=ModelDifficulty.HARD)

@dataclass(frozen=True)
class Config:
    """
    Configuration for the game.
    """
    NUM_GAMES: int = 1000
    PLAYER_A: Player = RANDOM_AGENT
    PLAYER_B: Player = REINFORCEMENT_AGENT_HARD

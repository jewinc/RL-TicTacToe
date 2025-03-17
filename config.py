from dataclasses import dataclass

from tictactoe.player import Player, HumanPlayer

from tictactoe.agents_collection.random_agent import RandomAgent
from tictactoe.agents_collection.minimax_agent import MinimaxAgent 

# Try importing ReinforcementAgent, but handle failure gracefully
try:
    from tictactoe.agents_collection.reinforcement_agent import ReinforcementAgent, ModelDifficulty
    RL_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    RL_AVAILABLE = False

HUMAN_ONE = HumanPlayer(name="Player A")
HUMAN_TWO = HumanPlayer(name="Player B")
RANDOM_AGENT = RandomAgent()
MINIMAX_AGENT = MinimaxAgent(use_alpha_beta=True)

# Define RL agents only if available
if RL_AVAILABLE:
    REINFORCEMENT_AGENT_EASY = ReinforcementAgent(model_difficulty=ModelDifficulty.EASY)
    REINFORCEMENT_AGENT_MEDIUM = ReinforcementAgent(model_difficulty=ModelDifficulty.MEDIUM)
    REINFORCEMENT_AGENT_HARD = ReinforcementAgent(model_difficulty=ModelDifficulty.HARD)

@dataclass(frozen=True)
class Config:
    """
    Configuration for the game.
    """
    # Pre-defined player configurations
    PLAYER_A = HumanPlayer("Player 1")
    PLAYER_B = RandomAgent()
    
    # Set up player options based on available agents
    if RL_AVAILABLE:
        PLAYER_OPTIONS = {
            "Human": lambda name: HumanPlayer(name),
            "Random": lambda _: RandomAgent(),
            "Minimax": lambda _: MinimaxAgent(use_alpha_beta=False),
            "Minimax (Alpha-Beta)": lambda _: MinimaxAgent(use_alpha_beta=True),
            "RL_Easy": lambda _: ReinforcementAgent(ModelDifficulty.EASY),
            "RL_Medium": lambda _: ReinforcementAgent(ModelDifficulty.MEDIUM),
            "RL_Hard": lambda _: ReinforcementAgent(ModelDifficulty.HARD),
        }
    else:
        # Fallback options without RL agents
        PLAYER_OPTIONS = {
            "Human": lambda name: HumanPlayer(name),
            "Random": lambda _: RandomAgent(),
            "Minimax": lambda _: MinimaxAgent(use_alpha_beta=False),
            "Minimax (Alpha-Beta)": lambda _: MinimaxAgent(use_alpha_beta=True),
        }
    
    # Game settings
    NUM_GAMES = 1 
    DEFAULT_MAX_GAMES = 10
    
    # Auto-play settings
    DEFAULT_MOVE_DELAY = 500  # milliseconds
    DEFAULT_GAME_DELAY = 1000  # milliseconds
    
    # GUI settings
    WINDOW_SIZE = "950x700"
    BOARD_SIZE = 3
    CELL_SIZE = 100
    
    # Colors
    BG_COLOR = "#f0f0f0"
    ACCENT_COLOR = "#4a7abc"
    X_COLOR = "#e74c3c"  # Red for X
    O_COLOR = "#3498db"  # Blue for O
    GRID_COLOR = "#2c3e50"
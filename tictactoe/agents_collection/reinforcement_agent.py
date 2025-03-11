import numpy as np

from enum import Enum

from tictactoe.agent import Agent, AgentType
from tictactoe.board import Symbol
from tictactoe.move import MoveType

from stable_baselines3 import PPO

class ModelDifficulty(Enum):
    EASY = "ppo_tictactoe_batch_1"
    MEDIUM = "ppo_tictactoe_batch_2"
    HARD = "ppo_tictactoe_batch_3"
    IMPOSSIBLE = "ppo_tictactoe_final"


class ReinforcementAgent(Agent):
    def __init__(self, model_difficulty: ModelDifficulty = ModelDifficulty.IMPOSSIBLE):
        super().__init__(AgentType.REINFORCEMENT)
        
        self.model = None
        self.model_difficulty = model_difficulty
        self.load_model(f"models/{model_difficulty.value}")

    def encode_board(self, board):
        """
        Convert the Tic-Tac-Toe board into a numerical representation for the RL model.
        Args:
            board (np.ndarray): 3x3 board
        Returns:
            np.ndarray: Encoded board
        """
        encoded_board = np.array(
            [
                1 if cell == Symbol.X else -1 if cell else 0
                for row in board
                for cell in row
            ]
        )
        return encoded_board.reshape(1, -1)  # Shape (1, 9)

    def choose_move(self, board) -> MoveType:
        """
        Choose the best move using the reinforcement learning model.
        Args:
            board (np.ndarray): 3x3 board
        Returns:
            MoveType: The chosen move
        """
        if self.model is None:
            raise ValueError("PPO model is not loaded!")

        loop_count = 0
        while True:
            observation = self.encode_board(board.get_board())
            action, _ = self.model.predict(observation)
            
            # Convert flat action index (0-8) to board coordinates (row, col)
            row, col = divmod(action, 3)
            move = MoveType((row, col))
            
            if board.is_move_valid(move):
                return move
            
            loop_count += 1
            if loop_count > 10:
                # Make a random choice if more than 10 loops done
                valid_moves = self.get_valid_moves(board)
                return np.random.choice(valid_moves)
    
    def load_model(self, path):
        """
        Load a trained PPO model from a file.
        Args:
            path (str): Path to the model file
        """
        self.model = PPO.load(path)
    
    def __str__(self):
        return f"{self.agent_type} ({self.model_difficulty.name})"
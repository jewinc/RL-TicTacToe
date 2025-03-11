import numpy as np

from tictactoe.agent import Agent, AgentType
from tictactoe.board import Symbol
from tictactoe.move import MoveType

from stable_baselines3 import PPO


class ReinforcementAgent(Agent):
    def __init__(self, symbol, model_path=None):
        super().__init__(AgentType.REINFORCEMENT, symbol)
        
        self.model = None
        if model_path:
            self.load_model(model_path)

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

        observation = self.encode_board(board.get_board())
        action, _ = self.model.predict(observation)
        
        # Convert flat action index (0-8) to board coordinates (row, col)
        row, col = divmod(action, 3)
        return MoveType((row, col))
    
    def load_model(self, path):
        """
        Load a trained PPO model from a file.
        Args:
            path (str): Path to the model file
        """
        self.model = PPO.load(path)
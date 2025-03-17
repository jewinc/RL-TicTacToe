import logging
import os
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

from enum import Enum

from tictactoe.agent import Agent, AgentType
from tictactoe.board import Symbol
from tictactoe.move import MoveType

# Import PPO conditionally to handle missing dependency
try:
    from stable_baselines3 import PPO
    PPO_AVAILABLE = True
except ImportError:
    PPO_AVAILABLE = False

class ModelDifficulty(Enum):
    EASY = "ppo_tictactoe_easy"
    MEDIUM = "ppo_tictactoe_medium"
    HARD = "ppo_tictactoe_hard"


class ReinforcementAgent(Agent):
    def __init__(self, model_difficulty: ModelDifficulty = ModelDifficulty.HARD):
        super().__init__(AgentType.REINFORCEMENT)
        
        self.model = None
        self.model_difficulty = model_difficulty
        self.load_model(f"models/{model_difficulty.value}.zip")

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
                1 if cell == Symbol.X else -1 if cell == Symbol.O else 0
                for row in board
                for cell in row
            ]
        )
        return encoded_board.reshape(1, -1)  # Shape (1, 9)

    def choose_move(self, board) -> MoveType:
        """
        Choose the best move using the reinforcement learning model if available,
        otherwise fallback to random selection.
        
        Args:
            board (np.ndarray): 3x3 board
        Returns:
            MoveType: The chosen move
        """
        valid_moves = self.get_valid_moves(board)
        
        if not valid_moves:
            raise ValueError("No valid moves left, but choose_move() was still called.")
            
        if self.model is None:
            # Fall back to random move if model is not loaded
            return random.choice(valid_moves)

        try:
            observation = self.encode_board(board.get_board())
            action, _ = self.model.predict(observation)

            row, col = divmod(action, 3)
            move = MoveType((row, col))

            if board.is_move_valid(move):
                return move
            else:
                # If predicted move is invalid, choose randomly from valid moves
                return random.choice(valid_moves)
                
        except Exception as e:
            logging.error(f"Error during model prediction: {e}")
            # Fallback to random if prediction fails
            return random.choice(valid_moves)
    
    def load_model(self, path):
        """
        Load a trained PPO model from a file.
        Args:
            path (str): Path to the model file
        """
        # Check if stable_baselines3 is available
        if not PPO_AVAILABLE:
            logging.warning("Stable Baselines 3 not available. Agent will play randomly.")
            self.model = None
            return
            
        if not os.path.exists(path):
            logging.warning(f"Model file not found: {path}. Agent will play randomly.")
            self.model = None  # Use a fallback random policy
            return
        
        try:
            self.model = PPO.load(path)
        except Exception as e:
            logging.error(f"Failed to load PPO model from {path}: {e}")
            self.model = None  # Ensure the agent doesn't attempt to use an invalid model
    
    def __str__(self):
        if self.model is None:
            return f"Reinforcement Agent (Fallback Random)"
        return f"Reinforcement Agent ({self.model_difficulty.name})"
import gymnasium as gym
import numpy as np

from gymnasium import spaces
from stable_baselines3 import PPO


class TicTacToeEnv(gym.Env):
    def __init__(self):
        super(TicTacToeEnv, self).__init__()
        self.observation_space = spaces.Box(low=-1, high=1, shape=(9,), dtype=np.int8)
        self.action_space = spaces.Discrete(9)
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros(9, dtype=np.int8)
        return self.board, {}

    def step(self, action):
        if self.board[action] != 0:
            return self.board, -10, True, False, {}  # Illegal move penalty

        self.board[action] = 1  # Assume the agent plays '1' and opponent '-1'

        if self.check_win(1):
            return self.board, 10, True, False, {}  # Agent wins
        elif np.all(self.board != 0):
            return self.board, 0, True, False, {}  # Draw

        # Opponent move (random)
        empty_spots = np.where(self.board == 0)[0]
        if empty_spots.size > 0:
            opp_move = np.random.choice(empty_spots)
            self.board[opp_move] = -1

        if self.check_win(-1):
            return self.board, -10, True, False, {}  # Opponent wins

        return self.board, 0, False, False, {}  # Game continues

    def check_win(self, player):
        win_states = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # Rows
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # Columns
            (0, 4, 8),
            (2, 4, 6),
        ]  # Diagonals
        return any(all(self.board[i] == player for i in state) for state in win_states)


env = TicTacToeEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=1000000)
model.save("ppo_tictactoe")

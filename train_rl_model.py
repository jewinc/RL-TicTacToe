import os
import random
import time
import gymnasium as gym
import numpy as np
import torch

from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.torch_layers import MlpExtractor


class TicTacToeEnv(gym.Env):
    def __init__(self):
        super(TicTacToeEnv, self).__init__()
        self.observation_space = spaces.Box(low=-1, high=1, shape=(9,), dtype=np.int8)
        self.action_space = spaces.Discrete(9)
        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = np.zeros(9, dtype=np.int8)
        self.done = False  # Explicitly track if game is done
        return self.board, {}  # Return initial state

    def get_opponent_model(self):
        """Load a fixed opponent model for consistent evaluation."""
        past_models = sorted(
            [f for f in os.listdir("./models") if "ppo_tictactoe_batch" in f],
            key=lambda f: int(f.split("_")[-1])  # Sort numerically by batch number
        )
        if past_models:
            latest_model = past_models[-1]  # Always load the most recent model
            return PPO.load(f"./models/{latest_model}")
        return None

    def step(self, action):
        if self.board[action] != 0:  # If action is invalid, force a valid choice
            empty_spots = np.where(self.board == 0)[0]
            if empty_spots.size > 0:
                action = np.random.choice(empty_spots)  # Pick a random valid move
            else:
                return self.board, -10, True, False, {}  # No moves left, shouldn't happen

        self.board[action] = 1  # Agent plays '1'

        if self.check_win(1):
            return self.board, 10, True, False, {}

        if np.all(self.board != 0):
            return self.board, 0, True, False, {}  # Draw

        # Opponent move
        opponent = self.get_opponent_model()
        if opponent:
            opponent_action, _ = opponent.predict(self.board, deterministic=True)
        else:
            empty_spots = np.where(self.board == 0)[0]
            opponent_action = np.random.choice(empty_spots) if empty_spots.size > 0 else None

        if opponent_action is not None:
            self.board[opponent_action] = -1
            if self.check_win(-1):
                return self.board, -10, True, False, {}

        # Encourage strategic positions
        reward = 0.1 if action in [0, 2, 4, 6, 8] else 0
        if action == 4:
            reward += 0.2  # Extra reward for center move

        return self.board, 0, False, False, {}

    def check_win(self, player):
        win_states = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)  # Diagonals
        ]
        return any(all(self.board[i] == player for i in state) for state in win_states)


# Create vectorized Tic-Tac-Toe environment
env = make_vec_env(TicTacToeEnv, n_envs=4)

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
env.seed(SEED)

# Define policy architecture
policy_kwargs = dict(
    net_arch=[128, 128],
    activation_fn=torch.nn.ReLU
)

# Initialize PPO model
model = PPO(
    "MlpPolicy",
    env,
    policy_kwargs=policy_kwargs,
    verbose=1,
    gamma=0.99,
    learning_rate=lambda f: 0.0003 * f,
    batch_size=64,
    n_steps=1024,
    ent_coef=0.05,
    clip_range=0.2,
    tensorboard_log="./ppo_tictactoe_log",
)

# Training time limit
TRAIN_TIME_SECONDS = 21600  # 6 hours

# Track time
start_time = time.time()
total_trained_timesteps = 0
batch_num = 0
timesteps_per_batch = 100_000

# Training loop (stops after 10 minutes)
while time.time() - start_time < TRAIN_TIME_SECONDS:
    model.learn(total_timesteps=timesteps_per_batch)
    total_trained_timesteps += timesteps_per_batch
    batch_num += 1
    model.save(f"./models/ppo_tictactoe_batch_{batch_num}")

print(f"Training stopped after {time.time() - start_time:.2f} seconds (~{total_trained_timesteps} timesteps).")

# Save final model
model.save("./models/ppo_tictactoe_final")

# Evaluate performance
obs = env.reset()
total_reward = np.zeros(env.num_envs)

for _ in range(10):  # Test over 10 games
    action, _ = model.predict(obs, deterministic=True)
    obs, rewards, dones, _, _ = env.step(action)
    total_reward += rewards

# Compute average reward
avg_reward = total_reward.mean() / 10
print(f"Final Model: Average Reward = {avg_reward}")
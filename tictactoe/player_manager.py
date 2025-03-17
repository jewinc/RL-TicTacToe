import logging
import random

from tictactoe.agent import Agent
from tictactoe.board import Symbol
from tictactoe.player import Player, PlayerType

from tictactoe.agents_collection.random_agent import RandomAgent
from tictactoe.agents_collection.reinforcement_agent import ReinforcementAgent, ModelDifficulty


class PlayerManager:
    def __init__(
        self,
        playerA: Player,
        playerB: Player,
    ):
        self.players = []
        self.current_player_idx = 0
        self.nb_human_players = sum(
            1 for player in (playerA, playerB) if player.player_type == PlayerType.HUMAN
        )
        
        self.players = [playerA, playerB]
        
        # Assigning symbols to players (in order)
        self.players[0].symbol = Symbol.X
        self.players[1].symbol = Symbol.O

    @property
    def current_player(self):
        return self.players[self.current_player_idx]

    def get_player_from_symbol(self, symbol: Symbol):
        if symbol == Symbol.EMPTY:
            return None
        for player in self.players:
            if player.symbol == symbol:
                return player
        logging.warning(f"Invalid symbol: {symbol}")
        return None

    def switch_player(self):
        self.current_player_idx = 1 - self.current_player_idx
    
    def reset(self):
        for player in self.players:
            player.reset()
        self.current_player_idx = 0

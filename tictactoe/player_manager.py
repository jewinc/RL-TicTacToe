import logging

from tictactoe.agent import AgentType
from tictactoe.board import Symbol
from tictactoe.player import HumanPlayer

from tictactoe.agents_collection.random_agent import RandomAgent


class PlayerManager:
    def __init__(
        self,
        agentA_type: AgentType = None,
        agentB_type: AgentType = None,
    ):
        self.players = []
        self.current_player_idx = 0

        # Determine the number of human players
        if agentA_type is None and agentB_type is None:
            self.nb_human_players = 2
        elif agentA_type is not None and agentB_type is not None:
            self.nb_human_players = 0
        else:
            self.nb_human_players = 1

        self.init_players(agentA_type, agentB_type)

    @property
    def current_player(self):
        return self.players[self.current_player_idx]

    @classmethod
    def get_player_from_symbol(cls, symbol: Symbol):
        if symbol == Symbol.EMPTY:
            return None
        for player in cls.players:
            if player.symbol == symbol:
                return player
        logging.warning(f"Invalid symbol: {symbol}")
        return None

    def init_players(
        self,
        agentA_type: AgentType = None,
        agentB_type: AgentType = None,
    ):
        if self.nb_human_players == 2:
            self.players.append(HumanPlayer(Symbol.X))
            self.players.append(HumanPlayer(Symbol.O))
        elif self.nb_human_players == 1:
            self.players.append(HumanPlayer(Symbol.X))
            self.players.append(
                self.init_machine_player(
                    (agentA_type if agentA_type is not None else agentB_type),
                    Symbol.O,
                )
            )
        else:
            self.players.append(self.init_machine_player(agentA_type, Symbol.X))
            self.players.append(self.init_machine_player(agentB_type, Symbol.O))

    def init_machine_player(self, agent_type: AgentType, symbol: Symbol):
        if agent_type == AgentType.RANDOM:
            return RandomAgent(symbol)
        # elif agent_type == AgentType.MINIMAX:
        #     return MinimaxPlayer()
        # elif agent_type == AgentType.REINFORCEMENT:
        #     return ReinforcementPlayer()
        else:
            logging.error(f"Invalid machine player type: {AgentType}")
            return None

    def switch_player(self):
        self.current_player_idx = 1 - self.current_player_idx

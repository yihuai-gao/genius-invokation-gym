"""Player & agent APIs
"""
from abc import ABC, abstractmethod
from typing import OrderedDict

from gisim.actions import Action

from gisim.classes.enums import PlayerID
from gisim.game import GameInfo


class Agent(ABC):
    def __init__(self, player_id: PlayerID):
        self.player_id = player_id

    @abstractmethod
    def take_action(self, game_info: OrderedDict) -> Action:
        pass


class AttackOnlyAgent(Agent):
    def __init__(self, player_id: PlayerID):
        super().__init__(player_id)

    def take_action(self, game_info: GameInfo) -> Action:
        # TODO: Only use normal attack in the game
        pass

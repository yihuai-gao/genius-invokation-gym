"""Player & agent APIs
"""
from abc import ABCMeta, abstractmethod
from typing import OrderedDict

from actions import *
from enum_classes import PlayerID


class Agent(ABCMeta):
    def __init__(self, player_id: PlayerID):
        self.PLAYER_ID = player_id

    @abstractmethod
    def take_action(self, game_info: OrderedDict) -> Action:
        pass

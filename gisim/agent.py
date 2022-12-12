'''Player & agent APIs
'''
from typing import OrderedDict
from enum_classes import PlayerID
from abc import ABCMeta, abstractmethod
from actions import *
class Agent(ABCMeta):
    def __init__(self, player_id:PlayerID):
        self.PLAYER_ID = player_id
        
    @abstractmethod
    def take_action(self, game_info:OrderedDict)->Action:
        pass
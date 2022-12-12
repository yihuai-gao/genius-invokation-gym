'''Judger class: determine legal moves of the current state
'''
from .actions import Action

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .game import Game
class Judge:
    def __init__(self, parent:'Game'):
        self._parent = parent
    
    def judge_action(self, player:int, action:Action):
        # TODO: judge the validity of a given action from the current state
        pass
    
    def get_legal_actions(self, player):
        pass
    
    def encode(self):
        # TODO: encode the judge status to dictionary
        pass
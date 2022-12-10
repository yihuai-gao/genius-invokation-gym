'''Judger class: determine legal moves of the current state
'''
from .game import Game
from .actions import Action
class Judger:
    def __init__(self, game:Game):
        self._game = game
    
    def publish_state(self, player:int):
        # TODO: return the current visible state for player 0(Viewer), 1, 2
        pass
    def judge_action(self, player:int, action:Action):
        # TODO: judge the validity of a given action from the current state
        pass
    
    def get_legal_actions(self, player):
        pass
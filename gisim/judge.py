"""Judger class: determine legal moves of the current state
"""
from typing import TYPE_CHECKING

from gisim.classes.enums import PlayerID

from gisim.classes.action import Action

if TYPE_CHECKING:
    from .game import Game


class Judge:
    def __init__(self, parent: "Game"):
        self._parent = parent

    def judge_action(self, player: PlayerID, action: Action):
        # TODO: judge the validity of a given action from the current state
        return True

    def get_legal_actions(self, player):
        pass

    def encode(self):
        # TODO: encode the judge status to dictionary
        pass

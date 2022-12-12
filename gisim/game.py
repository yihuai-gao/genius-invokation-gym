"""Genius Invokation Game class
"""
from collections import OrderedDict

from enum_classes import *
from numpy.random import RandomState

from .judge import Judge
from .player_area import PlayerArea


class Game:
    def __init__(self, player1_deck: dict, player2_deck: dict, seed: int = 50):
        self._random_state = RandomState(seed)
        self._status = GameStatus.INITIALIZING
        self._phase = InitializingPhase.CHANGE_CARD
        self._seed = seed
        self._active_player = self._random_state.randint(
            1, 3
        )  # Toss coin do determine player 1 or player 2
        self.judge = Judge(self, self._random_state)
        self.player1_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER1, deck=player1_deck
        )
        self.player2_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER2, deck=player2_deck
        )

    def encode_game(self, viewer_id: PlayerID):
        assert viewer_id in [0, 1, 2], "viewer_id should be one of 0 (judge), 1, 2"
        return OrderedDict(
            {
                "viewer_id": viewer_id,
                "status": self._status,
                "player1": self.player1_area.encode(viewer_id),
                "player2": self.player2_area.encode(viewer_id),
            }
        )

    def get_random_state(self):
        return self._random_state

"""Genius Invokation Game class
"""
from collections import OrderedDict

from numpy.random import RandomState

from gisim.classes.enums import *
from gisim.classes.status import StatusEntity
from gisim.classes.summon import Summon
from gisim.classes.support import Support

from .judge import Judge
from .player_area import PlayerArea


class Game:
    def __init__(self, player1_deck: dict, player2_deck: dict, seed: int = 50):
        self._random_state = RandomState(seed)
        self._status = GameStatus.INITIALIZING
        self._phase = Phase.CHANGE_CARD
        self._seed = seed
        self._active_player = self._random_state.choice(
            [1, 2]
        )  # Toss coin to determine who act first
        self.judge = Judge(self)
        self.player1_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER1, deck=player1_deck
        )
        self.player2_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER2, deck=player2_deck
        )

    def encode_game_info(self, viewer_id: PlayerID, use_dict=False):
        assert viewer_id in [0, 1, 2], "viewer_id should be one of 0 (judge), 1, 2"
        game_info_dict = OrderedDict(
            {
                "viewer_id": viewer_id,
                "status": self._status,
                "phase": self._phase,
                "active_player": self._active_player,
                "player1": self.player1_area.encode(viewer_id),
                "player2": self.player2_area.encode(viewer_id),
            }
        )
        if use_dict:
            return game_info_dict
        else:
            return GameInfo(game_info_dict)

    def get_random_state(self):
        return self._random_state


class PlayerInfo:
    def __init__(self, player_info_dict:OrderedDict):
        self.player_info_dict = player_info_dict
        self.player_id:PlayerID = player_info_dict["player_id"]
        self.hand_len:int = player_info_dict["hand"]["length"]
        self.hand:list = player_info_dict["hand"]["items"]
        self.deck_len:int = player_info_dict["deck"]["length"]
        self.deck:list[str] = player_info_dict["hand"]["items"]
        self.element_zone_len:int = player_info_dict["element_zone"]["length"]
        self.element_zone:list[ElementType] = player_info_dict["element_zone"]["items"]
        self.summon_zone:list[Summon] = player_info_dict["summon_zone"]
        self.support_zone:list[Support] = player_info_dict["support_zone"]
        self.status_zone:list[StatusEntity] = player_info_dict["status_zone"]
        
class GameInfo:
    def __init__(self, game_info_dict:OrderedDict):
        self.game_info_dict = game_info_dict
        self.viewer_id:PlayerID = game_info_dict["viewer_id"]
        self.status:GameStatus = game_info_dict["status"]
        self.phase:Phase = game_info_dict["phase"]
        self.active_player:PlayerID = game_info_dict["active_player"]
        self.player1:PlayerInfo = PlayerInfo(game_info_dict["player1"])
        self.player2:PlayerInfo = PlayerInfo(game_info_dict["player2"])
        
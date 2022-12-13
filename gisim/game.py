"""Genius Invokation Game class
"""
import os
from collections import OrderedDict
from queue import PriorityQueue
from random import Random
from typing import Optional

from gisim.classes.action import Action
from gisim.classes.enums import *
from gisim.classes.status import CombatStatusEntity
from gisim.classes.summon import Summon
from gisim.classes.support import Support

from .judge import Judge
from .player_area import PlayerArea


class Game:
    def __init__(
        self, player1_deck: dict, player2_deck: dict, seed: Optional[int] = None
    ):
        if seed is None:
            # Use system random to generate a seed if not provided
            seed = int.from_bytes(os.urandom(16), "big")

        self._seed = seed
        self._random_state = Random(seed)
        self.status = GameStatus.INITIALIZING
        self.phase = GamePhase.CHANGE_CARD
        self.active_player = PlayerID(
            self._random_state.choice([1, 2])
        )  # Toss coin to determine who act first
        self.judge = Judge(self)
        player1_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER1, deck=player1_deck
        )
        player2_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER2, deck=player2_deck
        )
        self.player_area = {PlayerID.PLAYER1:player1_area, PlayerID.PLAYER2:player2_area}
        self.msg_queue = PriorityQueue()

    def encode_game_info_dict(self, viewer_id: PlayerID):
        return OrderedDict(
            {
                "viewer_id": viewer_id,
                "status": self.status,
                "phase": self.phase,
                "active_player": self.active_player,
                "player1": self.player_area[PlayerID.PLAYER1].encode(viewer_id),
                "player2": self.player_area[PlayerID.PLAYER2].encode(viewer_id),
            }
        )

    def encode_game_info(self, viewer_id: Optional[PlayerID] = None):
        """Active player by default"""
        if viewer_id is None:
            viewer_id = self.active_player
        return GameInfo(self.encode_game_info_dict(viewer_id))

    def step(self, action: Action):
        
        pass
    

    def get_winner(self):
        # TODO
        pass

class CharacterInfo:
    def __init__(self, character_info_dict:OrderedDict):
        self.name:str = character_info_dict["name"]
        self.active:bool = character_info_dict["active"]
        self.alive:bool = character_info_dict["alive"]
        self.elemental_infusion:ElementType = character_info_dict["elemental_infusion"]
        self.elemental_attachment:ElementType = character_info_dict["elemental_attachment"]
        self.health_point:int = character_info_dict["health_point"]
        self.power:int = character_info_dict["power"]
        self.max_power:int = character_info_dict["max_power"]

class PlayerInfo:
    def __init__(self, player_info_dict: OrderedDict):
        self.player_info_dict = player_info_dict
        self.player_id: PlayerID = player_info_dict["player_id"]
        self.declared_end: bool = player_info_dict["declared_end"]
        self.hand_len: int = player_info_dict["hand"]["length"]
        self.hand: list = player_info_dict["hand"]["items"]
        self.deck_len: int = player_info_dict["deck"]["length"]
        self.deck: list[str] = player_info_dict["hand"]["items"]
        self.element_zone_len: int = player_info_dict["element_zone"]["length"]
        self.element_zone: list[ElementType] = player_info_dict["element_zone"]["items"]
        self.summon_zone: list[Summon] = player_info_dict["summon_zone"]
        self.support_zone: list[Support] = player_info_dict["support_zone"]
        self.combat_status_zone: list[CombatStatusEntity] = player_info_dict[
            "combat_status_zone"
        ]
        self.character_zone: list[CharacterInfo] = [CharacterInfo(player_info_dict["character_zone"][k]) for k in range(3)]
        self.active_character_position:CharacterPosition = player_info_dict["active_character_position"]


class GameInfo:
    def __init__(self, game_info_dict: OrderedDict):
        self.game_info_dict = game_info_dict
        self.viewer_id: PlayerID = game_info_dict["viewer_id"]
        self.status: GameStatus = game_info_dict["status"]
        self.phase: GamePhase = game_info_dict["phase"]
        self.active_player: PlayerID = game_info_dict["active_player"]
        self.player1: PlayerInfo = PlayerInfo(game_info_dict["player1"])
        self.player2: PlayerInfo = PlayerInfo(game_info_dict["player2"])
        
    def get_player_info(self, player_id:Optional[PlayerID]=None):
        if player_id is None:
            player_id = self.active_player
        if player_id == PlayerID.PLAYER1:
            return self.player1
        else:
            return self.player2
        
    def get_opponent_info(self):
        if self.active_player == PlayerID.PLAYER1:
            return self.player2
        else:
            return self.player1

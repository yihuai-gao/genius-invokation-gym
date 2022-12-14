"""Genius Invokation Game class
"""
import os
from collections import OrderedDict
from queue import PriorityQueue
from random import Random
from typing import Optional, cast

from .classes.action import *
from .classes.action import Action
from .classes.enums import *
from .classes.message import *
from .classes.status import CombatStatusEntity
from .classes.summon import Summon
from .classes.support import Support
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
        self.round_num = 1
        self.first_move_player = PlayerID(self._random_state.choice([1, 2]))
        """Toss coin to determine who act first for the first round;\n
        The early overed player will be the first_move_player for the next round"""
        self.active_player = self.first_move_player
        player1_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER1, deck=player1_deck
        )
        player2_area = PlayerArea(
            self, self._random_state, player_id=PlayerID.PLAYER2, deck=player2_deck
        )
        self.player_area = {
            PlayerID.PLAYER1: player1_area,
            PlayerID.PLAYER2: player2_area,
        }
        self.msg_queue = PriorityQueue()

    def encode_game_info_dict(self, viewer_id: PlayerID):
        return OrderedDict(
            {
                "viewer_id": viewer_id,
                "status": self.status,
                "phase": self.phase,
                "round_num": self.round_num,
                "first_move_player": self.first_move_player,
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

    def judge_action(self, action: Action):
        """The action can only be sent from the active player"""
        # TODO: judge the validity of a given action from the current state
        # Will send a
        return True

    def parse_action(self, action: Action):
        # Will take the elemental dice cost of the action and manage deck
        active_player = self.active_player

        if isinstance(action, ChangeCharacterAction):
            action = cast(ChangeCharacterAction, action)
            cost_msg = ChangeCharacterCostMsg(
                sender_id=active_player, position=action.position
            )
            self.msg_queue.put(cost_msg)
            self.process_msg_queue()
            msg = ChangeCharacterMsg(sender_id=active_player, position=action.position)
            self.msg_queue.put(msg)

        elif isinstance(action, ChangeCardsAction):
            action = cast(ChangeCardsAction, action)
            cards_idx: list[int] = action.cards_idx
            new_card_names = self.player_area[active_player].deck.draw_cards(
                len(cards_idx)
            )
            old_card_names = self.player_area[active_player].hand.remove_cards(
                cards_idx
            )
            self.player_area[active_player].hand.add_cards(new_card_names)
            self.player_area[active_player].deck.add_cards(old_card_names)

        elif isinstance(action, RollDiceAction):
            action = cast(RollDiceAction, action)
            self.player_area[active_player].dice_zone.reroll_dice(action.dice_idx)

        elif isinstance(action, DeclareEndAction):
            self.player_area[active_player].declare_end = True

        elif isinstance(action, UseCardAction):
            action = cast(UseCardAction, action)
            self.player_area[active_player].dice_zone.remove_dice(action.dice_idx)
            msg = UseCardMsg(
                sender_id=active_player,
                card_idx=action.card_idx,
                card_target=action.card_target,
            )
            self.msg_queue.put(msg)

        elif isinstance(action, ElementalTuningAction):
            action = cast(ElementalTuningAction, action)
            self.player_area[active_player].dice_zone.remove_dice([action.die_idx])
            target_element = self.player_area[
                active_player
            ].character_zone.active_character.element_type
            self.player_area[active_player].dice_zone.add_dice(1, target_element)

        elif isinstance(action, UseSkillAction):
            action = cast(UseSkillAction, action)
            msg = UseSkillMsg(
                sender_id=active_player,
                user_position=action.user_position,
                skill_name=action.skill_name,
                skill_target=action.skill_target,
            )
            self.msg_queue.put(msg)

    def process_msg_queue(self):
        pass

    def step(self, action: Action):
        self.parse_action(action)
        while True:
            if self.status == GameStatus.INITIALIZING:
                if self.phase == GamePhase.CHANGE_CARD:
                    self.active_player = ~self.active_player
                    if self.active_player != self.first_move_player:
                        # Wait for the other player to change cards
                        break
                    else:
                        # Both players have changed their cards
                        self.phase = GamePhase.SELECT_ACTIVE_CHARACTER
                        # Wait for players to select active character
                        break

                elif self.phase == GamePhase.SELECT_ACTIVE_CHARACTER:
                    self.process_msg_queue()  # The active character will be assigned

                    self.active_player = ~self.active_player
                    if self.active_player != self.first_move_player:
                        break
                    else:
                        # Both players have selected their character
                        # Finish initialization step
                        self.status = GameStatus.RUNNING
                        self.phase = GamePhase.ROUND_BEGIN

            elif self.status == GameStatus.RUNNING:
                if self.phase == GamePhase.ROUND_BEGIN:
                    self.msg_queue.put(RoundBeginMsg())
                    self.process_msg_queue()
                    # It seems that there is no player interaction in this phase

                    # Both player draw two cards by default
                    card_names = self.player_area[self.active_player].deck.draw_cards(2)
                    self.player_area[self.active_player].hand.add_cards(card_names)
                    card_names = self.player_area[~self.active_player].deck.draw_cards(
                        2
                    )
                    self.player_area[~self.active_player].hand.add_cards(card_names)

                    self.phase = GamePhase.ROLL_DICE
                    self.player_area[self.active_player].dice_zone.init_dice()
                    self.player_area[~self.active_player].dice_zone.init_dice()
                    # Wait for the first player to reroll dice
                    break

                elif self.phase == GamePhase.ROLL_DICE:
                    if (
                        self.player_area[
                            self.active_player
                        ].dice_zone.remaining_reroll_round
                        > 0
                    ):
                        # Let this player continue to reroll dices
                        break
                    # This player has run out of reroll chances
                    self.active_player = ~self.active_player
                    if self.active_player != self.first_move_player:
                        # Wait for the second player to reroll dice
                        break
                    else:
                        # Both players have rerolled dices
                        self.phase = GamePhase.PLAY_CARDS
                        # Wait for first_move_player to take action
                        break

                elif self.phase == GamePhase.PLAY_CARDS:
                    # Possible actions: UseCard, ElementalTuning, UseSkill, ChangeCharacter, DeclareEnd
                    # TODO: finish the reaction logic here
                    pass

    def get_winner(self):
        # TODO
        pass


class CharacterInfo:
    def __init__(self, character_info_dict: OrderedDict):
        self.name: str = character_info_dict["name"]
        self.active: bool = character_info_dict["active"]
        self.alive: bool = character_info_dict["alive"]
        self.elemental_infusion: ElementType = character_info_dict["elemental_infusion"]
        self.elemental_attachment: ElementType = character_info_dict[
            "elemental_attachment"
        ]
        self.health_point: int = character_info_dict["health_point"]
        self.power: int = character_info_dict["power"]
        self.max_power: int = character_info_dict["max_power"]


class PlayerInfo:
    def __init__(self, player_info_dict: OrderedDict):
        self.player_info_dict = player_info_dict
        self.player_id: PlayerID = player_info_dict["player_id"]
        self.declared_end: bool = player_info_dict["declared_end"]
        self.hand_len: int = player_info_dict["hand"]["length"]
        self.hand: list = player_info_dict["hand"]["items"]
        self.deck_len: int = player_info_dict["deck"]["length"]
        self.deck: list[str] = player_info_dict["hand"]["items"]
        self.dice_zone_len: int = player_info_dict["dice_zone"]["length"]
        self.dice_zone: list[ElementType] = player_info_dict["dice_zone"]["items"]
        self.summon_zone: list[Summon] = player_info_dict["summon_zone"]
        self.support_zone: list[Support] = player_info_dict["support_zone"]
        self.combat_status_zone: list[CombatStatusEntity] = player_info_dict[
            "combat_status_zone"
        ]
        self.character_zone: list[CharacterInfo] = [
            CharacterInfo(player_info_dict["character_zone"][k]) for k in range(3)
        ]
        self.active_character_position: CharacterPosition = player_info_dict[
            "active_character_position"
        ]


class GameInfo:
    def __init__(self, game_info_dict: OrderedDict):
        self.game_info_dict = game_info_dict
        self.viewer_id: PlayerID = game_info_dict["viewer_id"]
        self.status: GameStatus = game_info_dict["status"]
        self.phase: GamePhase = game_info_dict["phase"]
        self.round_num: int = game_info_dict["round_num"]
        self.active_player: PlayerID = game_info_dict["active_player"]
        self.first_move_player: PlayerID = game_info_dict["first_move_player"]
        self.player1: PlayerInfo = PlayerInfo(game_info_dict["player1"])
        self.player2: PlayerInfo = PlayerInfo(game_info_dict["player2"])

    def get_player_info(self, player_id: Optional[PlayerID] = None):
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

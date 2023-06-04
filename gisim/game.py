"""Genius Invokation Game class
"""
import os
from collections import OrderedDict
from queue import PriorityQueue,Queue
from random import Random
from typing import Dict, List, Optional, cast
import threading

from .classes.action import *
from .classes.action import Action
from .classes.enums import *
from .classes.message import *
from .classes.status import CombatStatusEntity
from .classes.summon import Summon
from .classes.support import Support
from .classes.reaction import *
from .player_area import BaseZone, PlayerArea, PlayerInfo


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
        self.winner = PlayerID.SPECTATOR
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

        self.service_queue = Queue()
        """服务队列是为某些事项提供服务的先入先出队列"""
    
    def service_process_handel(self):
        """服务处理事件会为所有玩家提供获取本局游戏对象的方法"""
        while True:
            msg: ServiceMessage = self.service_queue.get()



        


    def encode_game_info_dict(self, viewer_id: PlayerID):
        return OrderedDict(
            {
                "viewer_id": viewer_id,
                "status": self.status,
                "winner": self.winner,
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
            msg = PayChangeCharacterCostMsg(
                sender_id=active_player,
                target_pos=action.position,
                paid_dice_idx=action.dice_idx,
            )
            self.msg_queue.put(msg)
            active_character = self.player_area[active_player].active_character
            pos = (
                active_character.position
                if active_character is not None
                else CharPos.NONE
            )
            msg = ChangeCharacterMsg(
                sender_id=active_player,
                current_active=(active_player, pos),
                target=(active_player, action.position),
            )
            self.msg_queue.put(msg)
            if active_character is not None:
                change = active_character.character.alive
            else:
                change = True
            msg = AfterChangingCharacterMsg(
                sender_id=active_player,
                target=(active_player, action.position),
                change_active_player=change,
            )
            self.msg_queue.put(msg)

        elif isinstance(action, ChangeCardsAction):
            action = cast(ChangeCardsAction, action)
            msg = ChangeCardsMsg(
                sender_id=active_player,
                discard_cards_idx=action.cards_idx,
                draw_cards_type=[CardType.ANY for _ in action.cards_idx],
            )
            self.msg_queue.put(msg)

        elif isinstance(action, RollDiceAction):
            action = cast(RollDiceAction, action)
            msg = ChangeDiceMsg(
                sender_id=active_player,
                remove_dice_idx=action.dice_idx,
                new_target_element=[ElementType.ANY for _ in action.dice_idx],
                consume_reroll_chance=True,
            )
            self.msg_queue.put(msg)

        elif isinstance(action, DeclareEndAction):
            self.player_area[active_player].declare_end = True
            msg = DeclareEndMsg(sender_id=active_player)
            self.msg_queue.put(msg)

        elif isinstance(action, UseCardAction):
            action = cast(UseCardAction, action)
            msg = PayCardCostMsg(
                sender_id=active_player,
                card_idx=action.card_idx,
                card_user_pos=(active_player, action.card_user_pos),
                paid_dice_idx=action.dice_idx,
            )
            self.msg_queue.put(msg)
            msg = UseCardMsg(
                sender_id=active_player,
                card_user_pos=(active_player, action.card_user_pos),
                card_idx=action.card_idx,
                card_target=action.card_target,
            )
            self.msg_queue.put(msg)
            msg = AfterUsingCardMsg(
                sender_id=active_player,
                card_user_pos=action.card_user_pos,
                card_idx=action.card_idx,
                card_target=action.card_target,
                card_name="",  # To be initialized in HAND
                card_type=CardType.ANY,  # To be initialized in HAND
            )
            self.msg_queue.put(msg)

        elif isinstance(action, ElementalTuningAction):
            action = cast(ElementalTuningAction, action)
            active_character = self.player_area[active_player].active_character
            assert active_character is not None, "No active character selected"
            target_element = active_character.character.element_type
            msg = ChangeCardsMsg(
                sender_id=active_player,
                discard_cards_idx=[action.card_idx],
                draw_cards_type=[],
            )
            self.msg_queue.put(msg)
            msg = ChangeDiceMsg(
                sender_id=active_player,
                remove_dice_idx=[action.die_idx],
                new_target_element=[target_element],
            )
            self.msg_queue.put(msg)

        elif isinstance(action, UseSkillAction):
            action = cast(UseSkillAction, action)
            msg = PaySkillCostMsg(
                sender_id=self.active_player,
                user_pos=action.user_position,
                skill_name=action.skill_name,
                skill_targets=action.skill_targets,
                paid_dice_idx=action.dice_idx,
            )
            self.msg_queue.put(msg)
            msg = UseSkillMsg(
                sender_id=self.active_player,
                user_pos=action.user_position,
                skill_name=action.skill_name,
                skill_targets=action.skill_targets,
            )
            self.msg_queue.put(msg)
            msg = AfterUsingSkillMsg(
                sender_id=self.active_player,
                user_pos=action.user_position,
                skill_name=action.skill_name,
                skill_targets=action.skill_targets,
                elemental_reaction_triggered=ElementalReactionType.NONE,
            )
            self.msg_queue.put(msg)

    def process_msg_queue(self):
        while self.msg_queue.qsize() > 0:
            top_msg: Message = self.msg_queue.queue[0]
            updated = False
            respondent_zones = top_msg.respondent_zones
            zones = self.get_zones(respondent_zones)

            for zone in zones:
                updated = zone.msg_handler(self.msg_queue)
                if updated:
                    break
            if not updated:
                # All entities in the respondent zones does not respond to the message queue
                # For some special messages, game FSM should be updated
                top_msg: Message = self.msg_queue.queue[0]
                if isinstance(top_msg, RoundBeginMsg):
                    self.player_area[PlayerID.PLAYER1].declare_end = False
                    self.player_area[PlayerID.PLAYER2].declare_end = False

                if isinstance(top_msg, DeclareEndMsg):
                    self.player_area[top_msg.sender_id].declare_end = True
                    if self.player_area[~top_msg.sender_id].declare_end == False:
                        self.first_move_player = top_msg.sender_id

                self_ended = self.player_area[self.active_player].declare_end
                if self_ended:
                    # After changing dead character: if the player has declared end,
                    # the other player should continue playing
                    self.active_player = ~self.active_player
                else:
                    opponent_ended = self.player_area[~self.active_player].declare_end
                    if (
                        top_msg.change_active_player
                        and not opponent_ended
                        and self.active_player == top_msg.sender_id
                    ):
                        self.active_player = ~self.active_player
                # TODO: Other impact on the game FSM
                self.msg_queue.get()
                if isinstance(top_msg, CharacterDiedMsg):
                    top_msg = cast(CharacterDiedMsg, top_msg)
                    # TODO: Determine whether game ends
                    # Wait for the player to change character
                    self.active_player = top_msg.target[0]
                    char_died = top_msg.target[0]
                    # Wait for player to select the next active character
                    return char_died

        return False

    def get_zones(self, zones: List[Tuple[PlayerID, RegionType]]):
        zone_pointers: List[BaseZone] = []
        for player_id, zone_type in zones:
            zone_pointers += self.player_area[player_id].get_zones(zone_type)
        # Remove empty zones (e.g. no active character)
        return [pointers for pointers in zone_pointers if pointers is not None]

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

                    # self.active_player = ~self.active_player
                    if self.active_player != self.first_move_player:
                        break
                    else:
                        # Both players have selected their character
                        # Finish initialization step
                        self.status = GameStatus.RUNNING
                        self.phase = GamePhase.ROUND_BEGIN

            elif self.status == GameStatus.RUNNING:
                if self.phase == GamePhase.ROUND_BEGIN:
                    self.msg_queue.put(
                        RoundBeginMsg(first_move_player=self.first_move_player)
                    )
                    self.process_msg_queue()
                    # It seems that there is no player interaction in this phase

                    self.phase = GamePhase.ROLL_DICE

                    self.player_area[self.active_player].dice_zone.init_dice()
                    self.player_area[~self.active_player].dice_zone.init_dice()
                    # Wait for the first player to reroll dice
                    break

                elif self.phase == GamePhase.ROLL_DICE:
                    self.process_msg_queue()
                    if (
                        self.player_area[
                            self.active_player
                        ].dice_zone.remaining_reroll_chance
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
                    char_died = self.process_msg_queue()
                    if char_died:
                        # Character died when processing message queue
                        # Check whether all characters died
                        current_player = self.active_player
                        char_alive = [
                            ch.character.alive
                            for ch in self.player_area[current_player].character_zones
                        ]
                        if not any(char_alive):
                            self.status = GameStatus.ENDED
                            self.winner = ~current_player
                        break
                    if (
                        self.player_area[PlayerID.PLAYER1].declare_end
                        and self.player_area[PlayerID.PLAYER2].declare_end
                    ):
                        # Both players have declared end
                        self.phase = GamePhase.ROUND_END
                        self.active_player = self.first_move_player
                        self.msg_queue.put(
                            RoundEndMsg(first_move_player=self.first_move_player)
                        )
                    else:
                        break

                elif self.phase == GamePhase.ROUND_END:
                    if self.msg_queue.qsize() > 0:
                        char_died = self.process_msg_queue()
                        if char_died:
                            # Character died when processing message queue
                            # Check whether all characters died
                            current_player = self.active_player
                            char_alive = [
                                ch.character.alive
                                for ch in self.player_area[
                                    current_player
                                ].character_zones
                            ]
                            if not any(char_alive):
                                self.status = GameStatus.ENDED
                                self.winner = ~current_player
                            break
                    else:
                        # All calculations are done
                        self.round_num += 1
                        self.phase = GamePhase.ROUND_BEGIN
                        self.active_player = self.first_move_player


class GameInfo:
    def __init__(self, game_info_dict: OrderedDict):
        self.game_info_dict = game_info_dict
        self.viewer_id: PlayerID = game_info_dict["viewer_id"]
        self.winner: PlayerID = game_info_dict["winner"]
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

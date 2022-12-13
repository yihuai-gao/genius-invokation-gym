"""Judger class: determine legal moves of the current state
"""
from queue import PriorityQueue
from typing import TYPE_CHECKING, cast

from classes.message import ChangeCardsMsg, RollDiceMsg, UseCardMsg, UseSkillMsg

from gisim.classes.action import (
    Action,
    ChangeCardsAction,
    ChangeCharacterAction,
    DeclareEndAction,
    ElementalTuningAction,
    RollDiceAction,
    UseCardAction,
    UseSkillAction,
)
from gisim.classes.enums import ActionType, CardType, ElementType, PlayerID

if TYPE_CHECKING:
    from .game import Game
from typing import Type


class Judge:
    def __init__(self, parent: "Game"):
        self._parent = parent

    def judge_action(self, action: Action):
        """The action can only be sent from the active player"""
        # TODO: judge the validity of a given action from the current state
        return True

    def parse_action(self, action: Action, msg_queue: PriorityQueue):
        # Will take the elemental dice cost of the action and manage deck
        active_player = self._parent.active_player

        if action.action_type == ActionType.ChangeCharacter:
            pass

        elif action.action_type == ActionType.ChangeCards:
            action = cast(ChangeCardsAction, action)
            cards_idx: list[int] = action.cards_idx
            msg = ChangeCardsMsg(
                sender_id=active_player,
                discard_cards_idx=cards_idx,
                draw_cards_type=[CardType.ANY],
            )
            msg_queue.put(msg)

        elif action.action_type == ActionType.RollDice:
            action = cast(RollDiceAction, action)
            self._parent.player_area[active_player].element_zone.remove_dice(
                action.dice_idx
            )
            self._parent.player_area[active_player].element_zone.add_dice(
                dice_num=len(action.dice_idx)
            )

        elif action.action_type == ActionType.DeclareEnd:
            self._parent.player_area[active_player].declare_end = True

        elif action.action_type == ActionType.UseCard:
            action = cast(UseCardAction, action)
            self._parent.player_area[active_player].element_zone.remove_dice(
                action.dice_idx
            )
            msg = UseCardMsg(
                sender_id=active_player,
                card_idx=action.card_idx,
                card_target=action.card_target,
            )

        elif action.action_type == ActionType.ElementalTuning:
            action = cast(ElementalTuningAction, action)
            self._parent.player_area[active_player].element_zone.remove_dice(
                [action.die_idx]
            )
            target_element = self._parent.player_area[
                active_player
            ].character_zone.active_character.element_type
            self._parent.player_area[active_player].element_zone.add_dice(
                1, target_element
            )

        elif action.action_type == ActionType.UseSkill:
            action = cast(UseSkillAction, action)
            msg = UseSkillMsg(
                sender_id=active_player,
                user_position=action.user_position,
                skill_name=action.skill_name,
                skill_target=action.skill_target,
            )

    def get_legal_actions(self, player):
        pass

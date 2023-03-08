""" Interface between the game environment and players(agents)

Start Game: ChangeCharacter (Also happens when the active character falls), ChangeCards

In each round: RerollDice (also happens after using some cards, e.g. 乾坤一掷)
    Combat Action: UseSkill, ChangeCharacter, DeclareEnd
    Fast Action: UseCard, ElementalTuning

"""

from abc import ABC
from typing import List, Tuple
from pydantic import BaseModel

from gisim.classes.entity import Entity
from gisim.classes.enums import CharPos, EntityType, PlayerID


class Action(Entity, ABC):
    """Action includes cost information."""

    def _check_cards_index(self, cards_idx: List[int]):
        assert type(cards_idx) == list
        for card in cards_idx:
            assert type(card) == int and card >= 0

    def _check_dice_index(self, dice_idx):
        assert type(dice_idx) == list
        for die_idx in dice_idx:
            assert type(die_idx) == int and die_idx >= 0


class ChangeCharacterAction(Action):
    position: CharPos
    dice_idx: List[int]


class ChangeCardsAction(Action):
    cards_idx: List[int]


class RollDiceAction(Action):
    dice_idx: List[int]


class UseSkillAction(Action):
    user_position: CharPos
    skill_name: str
    dice_idx: List[int]
    skill_targets: List[Tuple[PlayerID, CharPos]]


class DeclareEndAction(Action):
    pass


class UseCardAction(Action):
    card_idx: int
    dice_idx: List[int]
    card_target: List[Tuple[PlayerID, EntityType, int]]
    card_user_pos: CharPos


class ElementalTuningAction(Action):
    card_idx: int
    die_idx: int

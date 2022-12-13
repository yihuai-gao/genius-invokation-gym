""" Interface between the game environment and players(agents)

Start Game: ChangeCharacter (Also happens when the active character falls), ChangeCards

In each round: RerollDice (also happens after using some cards, e.g. 乾坤一掷)
    Combat Action: UseSkill, ChangeCharacter, DeclareEnd
    Fast Action: UseCard, ElementalTuning

"""

from abc import ABC, abstractmethod

from gisim.classes.enums import CharacterPosition, PlayerID

from .entity import Entity
from pydantic import BaseModel


class Action(Entity, BaseModel, ABC):
    """Action includes cost information."""

    def _check_cards_index(self, cards_idx: list[int]):
        assert type(cards_idx) == list
        for card in cards_idx:
            assert type(card) == int and card >= 0

    def _check_dice_index(self, dice_idx):
        assert type(dice_idx) == list
        for die_idx in dice_idx:
            assert type(die_idx) == int and die_idx >= 0


class ChangeCharacterAction(Action):
    position: CharacterPosition


class ChangeCardsAction(Action):
    cards_idx: list[int]


class RollDiceAction(Action):
    dice_idx: list[int]


class UseSkillAction(Action):
    user_position: CharacterPosition
    skill_name: str
    dice_idx: list[int]
    skill_target: list[tuple[PlayerID, CharacterPosition]]


class DeclareEndAction(Action):
    pass


class UseCardAction(Action):
    card_idx: int
    dice_idx: list[int]
    card_target: list[tuple[PlayerID, CharacterPosition]]


class ElementalTuningAction(Action):
    card_idx: int
    die_idx: int

"""Message classes for communication and calculation
"""

from abc import ABC, abstractmethod
from ast import Param
from typing import Optional
from uuid import UUID
from typing import ParamSpec
from pydantic import BaseModel, root_validator

from .entity import Entity
from .enums import (
    CardType,
    CharPos,
    ElementType,
    MsgPriority,
    PlayerID,
    RegionType,
)


class Message(BaseModel, Entity, ABC):
    """Abstract base class of different kinds of messages"""

    sender_id: PlayerID
    priority: MsgPriority
    remaining_respondent_zones: list[tuple[PlayerID, CharPos, RegionType]] = []
    """The message will travel all listed zones for respond. """
    responded_entities: list[UUID] = []
    """The UUID of all responded entities"""

    def __lt__(self, other: "Message"):
        return self.priority < other.priority


class MessageReceiver(ABC):
    """Abstract base class of different kinds of message receivers"""

    @abstractmethod
    def on_message(self, msg: Message):
        ...


# Immediate operations


class GenerateSummonMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    pass


class RemoveSummonMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    pass


class GenerateSupportMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    pass


class GenerateCharacterStatusMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    pass


class GenerateCombatStatusMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    pass


class GenerateEquipmentMsg(Message):
    "Usually generated from Cards"
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    pass


class ChangeCardsMsg(Message):
    """Send from Agent/Card/Support/...
    Include both discard cards and drawing cards."""

    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    discard_cards_idx: list[int]
    draw_cards_type: list[CardType]
    """If no type specified, use `CardType.ANY`"""
    change_player: bool = False


# Drawing card/Changing Dice related
class ChangeDiceMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    remove_dice_idx: list[int]
    """Index of dice to be removed"""
    new_target_element: list[ElementType]
    """Number of elements should be the same as number of dice to be generated.\n
    Target element: 
        ElementType.ANY represents a random dice among 7 element types (e.g. dice generated from 元素质变仪)\n
        ElementType.NONE represents a random dice among 8 kinds of dice (including the OMNI element)"""

    @property
    def remaining_respondent_zones(self):
        return [(self.sender_id, CharPos.NONE, RegionType.DICE_ZONE)]


class ChangeCardMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    remove_cards_idx = list[int]
    """Index of cards to be removed"""
    new_cards_type = list[CardType]

    @property
    def remaining_respondent_zones(self):
        return [(self.sender_id, CharPos.NONE, RegionType.HAND)]


# Calculate cost related messages


class PayCostMsg(Message, ABC):
    priority: MsgPriority = MsgPriority.PAY_COST
    simulate: bool = False
    required_cost: dict[ElementType, int] = {}
    """Required cost of this action. Will be affected by equipment/character status/
    combat status/support"""
    paid_cost: dict[ElementType, int] = {}
    """What the user actual paid."""


class PayCardCostMsg(PayCostMsg):

    """Will calculate and remove the cost before processing `UseCardMsg`"""

    card_idx: int
    card_user_pos: CharPos
    """The user of the card. e.g. talent card"""
    card_target: list[tuple[PlayerID, CharPos]]
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""

    @root_validator
    def init_remaining_respondent_zones(cls, values):
        default_zones = [
            (values["sender_id"], CharPos.NONE, RegionType.HAND),
            (values["sender_id"], values["card_user_pos"], RegionType.CHAR_ZONE),
            (values["sender_id"], CharPos.NONE, RegionType.COMBAT_STATUS_ZONE),
            (values["sender_id"], CharPos.NONE, RegionType.SUPPORT_ZONE),
            (values["sender_id"], CharPos.NONE, RegionType.DICE_ZONE),
        ]
        if not values["remaining_respondent_zones"]:
            values["remaining_respondent_zones"] = default_zones
        return values


class PaySkillCostMsg(Message):
    """Will calculate and remove the cost before processing `UseSkillMsg`"""

    priority: MsgPriority = MsgPriority.PAY_COST
    user_position: CharPos
    skill_name: str
    skill_target: list[tuple[PlayerID, CharPos]]
    simulate: bool = False
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""
    cost: dict[ElementType, int] = {}

    @root_validator
    def init_remaining_respondent_zones(cls, values):
        default_zones = [
            (values["sender_id"], CharPos.ACTIVE, RegionType.EQUIPMENT_ZONE),
            (values["sender_id"], CharPos.ACTIVE, RegionType.STATUS_ZONE),
            (values["sender_id"], CharPos.NONE, RegionType.COMBAT_STATUS_ZONE),
            (values["sender_id"], CharPos.NONE, RegionType.SUPPORT_ZONE),
            (values["sender_id"], CharPos.NONE, RegionType.DICE_ZONE),
        ]
        if not values["remaining_respondent_zones"]:
            values["remaining_respondent_zones"] = default_zones
        return values


class PayChangeCharacterCostMsg(Message):
    priority: MsgPriority = MsgPriority.PAY_COST
    position: CharPos
    simulate: bool = False
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""


# Player action related.
# After player agent submits an `Action`, `game.judge_action`` will first check its validity
# then convert the action to the corresponding message.


class ChangeCharacterMsg(Message):
    """Send from Agent/Character(Skill, Elemental Reaction)"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    position: CharPos

    @property
    def remaining_respondent_zones(self):
        return [(self.sender_id,)]


class UseCardMsg(Message):
    """Send from Agent"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    card_idx: int
    card_target: list[tuple[PlayerID, CharPos]]


class UseSkillMsg(Message):
    """Send from Agent"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    user_position: CharPos
    skill_name: str
    skill_target: list[tuple[PlayerID, CharPos]]
    """In case one character can assign multiple targets in the future"""

    @property
    def remaining_respondent_zones(self):
        return [
            (self.sender_id, RegionType.HAND),
            (
                self.sender_id,
                RegionType.CHAR_ZONE,
            ),  # the card may not be used by the active character (e.g. 刻晴的雷楔)
            (self.sender_id, RegionType.COMBAT_STATUS_ZONE),
            (
                ~self.sender_id,
                RegionType.CHAR_ZONE,
            ),  # the damage has not been generated yet
            (~self.sender_id, RegionType.COMBAT_STATUS_ZONE),
            (~self.sender_id, RegionType.SUMMON_ZONE),
            (
                ~self.sender_id,
                RegionType.CHAR_ZONE,
            ),  # generate damage and then generate
        ]


# Hp related
# This kind of message is usually responded by a lot of entities, from the current character/summon to its target


class DealDamageMsg(Message):
    """Send from Character(Skill)/Character Status/Summon/Combat Status"""

    priority: MsgPriority = MsgPriority.GENERAL_EFFECT
    target: list[tuple[PlayerID, CharPos, ElementType, int]]
    pass


class HurtMsg(Message):
    """Send from Character/Summon who is being attacked and all other effects are already calculated"""

    priority: MsgPriority = MsgPriority.GENERAL_EFFECT
    pass


class RecoverHpMsg(Message):
    """Send from Card/Character(Skill)/Equipment/Support/Summon/..."""

    priority: MsgPriority = MsgPriority.GENERAL_EFFECT
    pass


# Special types


class ElementalReactionEffectMsg(Message):
    """Send from Character(under attack)/Summon"""

    priority: MsgPriority = MsgPriority.ELEMENTAL_REACTION_EFFECT
    pass


class CharacterDiedMsg(Message):
    """Send from Character(under attack)"""

    priority: MsgPriority = MsgPriority.HP_CHANGED
    pass


# Game status related
# A lot of entities will be responded by these messages
# This message will not disappear when traveling through entities. It serves as a finite-state machine for Game


class RoundBeginMsg(Message):
    """Send from Game"""

    priority: MsgPriority = MsgPriority.GAME_STATUS
    sender_id: PlayerID = PlayerID.SPECTATOR
    pass


class RoundEndMsg(Message):
    """Send from Game"""

    priority: MsgPriority = MsgPriority.GAME_STATUS
    sender_id: PlayerID = PlayerID.SPECTATOR
    pass

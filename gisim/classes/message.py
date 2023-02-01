"""Message classes for communication and calculation
"""

import itertools
from abc import ABC, abstractmethod
from ast import Param
from typing import Optional, ParamSpec
from uuid import UUID

from pydantic import BaseModel, root_validator

from .entity import Entity
from .enums import (
    CardType,
    CharPos,
    ElementalReactionType,
    ElementType,
    EntityType,
    MsgPriority,
    PlayerID,
    RegionType,
)


class Message(Entity, ABC):
    """Abstract base class of different kinds of messages"""

    _id_counter = itertools.count()
    """A static counter to create increasing ID"""

    _msg_id: int = -1
    sender_id: PlayerID
    priority: MsgPriority
    respondent_zones: list[tuple[PlayerID, RegionType]] = []
    """The message will travel all listed zones for respond. It will travel all zones by default as in the root validator"""
    responded_entities: list[UUID] = []
    """The UUID of all responded entities"""
    change_active_player: bool = False

    def __lt__(self, other: "Message"):
        if self.priority == other.priority:
            return (
                self._msg_id < other._msg_id
            )  # The earlier message should have the higher priority
        else:
            return self.priority < other.priority

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.ALL),
                (~values["sender_id"], RegionType.ALL),
            ]
        values["_msg_id"] = next(Message._id_counter)  # Add message id
        return values


# Immediate operations


class GenerateSummonMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    summon_name: str
    target_id: PlayerID = PlayerID.SPECTATOR
    """Will be set to the sender_id by default; It can also be the opponent's id in special cases"""

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["target_id"] or values["target_id"] == PlayerID.SPECTATOR:
            values["target_id"] = values["sender_id"]
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["target_id"], RegionType.SUMMON_ZONE),
            ]
        return values


class RemoveSummonMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    summon_name: str

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.SUMMON_ZONE),
            ]
        return values


class GenerateSupportMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    support_name: str

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.SUPPORT_ZONE),
            ]
        return values


class GenerateCharacterStatusMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    target: tuple[PlayerID, CharPos]
    status_name: str
    # remaining_round: int

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["target"][0], RegionType(values["target"][1].value)),
            ]
        return values


class GenerateCombatStatusMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    target_player_id: PlayerID
    combat_status_name: str

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["target_player_id"], RegionType.COMBAT_STATUS_ZONE),
            ]
        return values


class GenerateEquipmentMsg(Message):
    "Usually generated from Cards"
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    target: tuple[PlayerID, CharPos]
    equipment_name: str

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["player_id"], RegionType(values["target_char_pos"].value)),
            ]
        return values


class ChangeCardsMsg(Message):
    """Send from Agent/Card/Support/...
    Include both discard cards and drawing cards."""

    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    discard_cards_idx: list[int]
    draw_cards_type: list[CardType]
    """If no type specified, use `CardType.ANY`"""

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.CARD_ZONE),
            ]
        return values


# Changing Dice related
class ChangeDiceMsg(Message):
    priority: MsgPriority = MsgPriority.IMMEDIATE_OPERATION
    remove_dice_idx: list[int]
    """Index of dice to be removed"""
    new_target_element: list[ElementType]
    """Number of elements should be the same as number of dice to be generated.\n
    Target element: 
        ElementType.BASIC represents a random dice among 7 element types (e.g. dice generated from 元素质变仪)\n
        ElementType.ANY represents a random dice among 8 kinds of dice (including the OMNI element)"""
    consume_reroll_chance: bool = False
    update_max_reroll_chance: Optional[int] = None

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.DICE_ZONE),
            ]
        return values


# Calculate cost related messages


class PayCostMsg(Message, ABC):
    priority: MsgPriority = MsgPriority.PAY_COST
    simulate: bool = False
    required_cost: dict[ElementType, int] = {}
    """Required cost of this action. Will be affected by equipment/character status/
    combat status/support"""
    paid_dice_idx: list[int] = []
    """What the user actual paid."""


class PayCardCostMsg(PayCostMsg):

    """Will calculate and remove the cost before processing `UseCardMsg`"""

    card_idx: int
    card_user_pos: CharPos
    """The user of the card. e.g. talent card"""

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.CARD_ZONE),
                (values["sender_id"], RegionType(values["card_user_pos"].value)),
                (values["sender_id"], RegionType.COMBAT_STATUS_ZONE),
                (values["sender_id"], RegionType.SUPPORT_ZONE),
                (values["sender_id"], RegionType.DICE_ZONE),
            ]
        return values


class PaySkillCostMsg(PayCostMsg):
    """Will calculate and remove the cost before processing `UseSkillMsg`"""

    priority: MsgPriority = MsgPriority.PAY_COST
    user_pos: CharPos
    skill_name: str
    skill_targets: list[tuple[PlayerID, CharPos]]
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.CHARACTER_ACTIVE),
                (values["sender_id"], RegionType.COMBAT_STATUS_ZONE),
                (values["sender_id"], RegionType.SUPPORT_ZONE),
                (values["sender_id"], RegionType.DICE_ZONE),
            ]
        return values


class PayChangeCharacterCostMsg(PayCostMsg):
    priority: MsgPriority = MsgPriority.PAY_COST
    target_pos: CharPos
    simulate: bool = False
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["sender_id"], RegionType.CHARACTER_ACTIVE),
                (values["sender_id"], RegionType.COMBAT_STATUS_ZONE),
                (values["sender_id"], RegionType.SUPPORT_ZONE),
                (values["sender_id"], RegionType.DICE_ZONE),
            ]
        return values


# Player action related.
# After player agent submits an `Action`, `game.judge_action`` will first check its validity
# then convert the action to the corresponding message.


class ChangeCharacterMsg(Message):
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    current_active: tuple[PlayerID, CharPos]
    target: tuple[PlayerID, CharPos]

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["target"][0], RegionType.CHARACTER_ALL),
                (values["target"][0], RegionType.COMBAT_STATUS_ZONE),
                (values["target"][0], RegionType.SUPPORT_ZONE),
            ]
        return values


class UseCardMsg(Message):
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    card_idx: int
    card_target: list[tuple[PlayerID, EntityType, int]]
    card_user_pos: CharPos


class UseSkillMsg(Message):
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    user_pos: CharPos
    skill_name: str
    skill_targets: list[tuple[PlayerID, CharPos]]
    """In case one character can assign multiple targets in the future"""


class AfterUsingSkillMsg(Message):
    priority: MsgPriority = MsgPriority.ACTION_DONE
    user_pos: CharPos
    skill_name: str
    skill_targets: list[tuple[PlayerID, CharPos]]
    elemental_reaction_triggered: ElementalReactionType
    change_active_player: bool = True


class AfterUsingCardMsg(Message):
    priority: MsgPriority = MsgPriority.ACTION_DONE
    card_name: str
    card_user_pos: CharPos
    card_target: list[tuple[PlayerID, EntityType, int]]
    card_type: CardType  # For 便携营养袋
    card_idx: int


class AfterChangingCharacterMsg(Message):
    priority: MsgPriority = MsgPriority.ACTION_DONE
    target: tuple[PlayerID, CharPos]
    change_active_player: bool = True


class DeclareEndMsg(Message):
    priority: MsgPriority = MsgPriority.ACTION_DONE
    change_active_player: bool = True
    respondent_zones: list[tuple[PlayerID, RegionType]] = []


# Changing hp/power/ related
# This kind of message is usually responded by a lot of entities, from the current character/summon to its target


class DealDamageMsg(Message):
    """Send from Character(Skill)/Character Status/Summon/Combat Status"""

    priority: MsgPriority = MsgPriority.GENERAL_EFFECT
    attacker: tuple[PlayerID, CharPos]
    """If the damage is generated by summon, CharPos should be set to CharPos.NONE"""
    targets: list[tuple[PlayerID, CharPos, ElementType, int]]
    elemental_reaction_triggered: ElementalReactionType = ElementalReactionType.NONE
    """Will be modified if elemental reaction is triggered"""
    all_buffs_included = False
    """Whether every attack/defense buffs are included"""


class AttachElementMsg(Message):
    """Send from Character/Summon who is being attacked and all other effects are already calculated"""

    priority: MsgPriority = MsgPriority.GENERAL_EFFECT
    targets: list[tuple[PlayerID, CharPos]]
    element_types: list[ElementType]


class HealHpMsg(Message):
    """Send from Card/Character(Skill)/Equipment/Support/Summon/..."""

    priority: MsgPriority = MsgPriority.GENERAL_EFFECT
    targets: list[tuple[PlayerID, CharPos, int]]


class ChangePowerMsg(Message):
    priority: MsgPriority = MsgPriority.GENERAL_EFFECT
    change_targets: list[tuple[PlayerID, CharPos]]
    change_vals: list[int]

    @root_validator
    def init_respondent_zones(cls, values):
        change_vals: list[int] = values["change_vals"]
        change_targets: list[tuple[PlayerID, CharPos]] = values["change_targets"]

        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (target[0], RegionType(target[1].value)) for target in change_targets
            ]
        return values


# HP changed


# Special types


class ElementalReactionTriggeredMsg(Message):
    """Send from Character(under attack)/Summon"""

    priority: MsgPriority = MsgPriority.ELEMENTAL_REACTION_EFFECT
    elemental_reaction_type: ElementalReactionType
    target: tuple[PlayerID, CharPos]


class CharacterDiedMsg(Message):
    """Send from Character(under attack)"""

    priority: MsgPriority = MsgPriority.HP_CHANGED
    target: tuple[PlayerID, CharPos]

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            target: tuple[PlayerID, CharPos] = values["target"]
            values["respondent_zones"] = [
                (target[0], RegionType(target[1].value)),  # 本大爷
                (~target[0], RegionType.CHARACTER_ACTIVE),  # 赌徒
            ]
        return values


# Game status related
# A lot of entities will be responded by these messages
# This message will not disappear when traveling through entities. It serves as a finite-state machine for Game


class RoundBeginMsg(Message):
    """Send from Game"""

    priority: MsgPriority = MsgPriority.GAME_STATUS
    sender_id: PlayerID = PlayerID.SPECTATOR
    first_move_player: PlayerID

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["first_move_player"], RegionType.SUMMON_ZONE),
                (values["first_move_player"], RegionType.SUPPORT_ZONE),
                (values["first_move_player"], RegionType.CHARACTER_ALL),
                (values["first_move_player"], RegionType.COMBAT_STATUS_ZONE),
                (~values["first_move_player"], RegionType.SUMMON_ZONE),
                (~values["first_move_player"], RegionType.SUPPORT_ZONE),
                (~values["first_move_player"], RegionType.CHARACTER_ALL),
                (~values["first_move_player"], RegionType.COMBAT_STATUS_ZONE),
            ]
        return values


class RoundEndMsg(Message):
    """Send from Game"""

    priority: MsgPriority = MsgPriority.GAME_STATUS
    sender_id: PlayerID = PlayerID.SPECTATOR
    first_move_player: PlayerID

    @root_validator
    def init_respondent_zones(cls, values):
        if not values["respondent_zones"]:
            values["respondent_zones"] = [
                (values["first_move_player"], RegionType.SUMMON_ZONE),
                (values["first_move_player"], RegionType.SUPPORT_ZONE),
                (values["first_move_player"], RegionType.CHARACTER_ALL),
                (values["first_move_player"], RegionType.COMBAT_STATUS_ZONE),
                (~values["first_move_player"], RegionType.SUMMON_ZONE),
                (~values["first_move_player"], RegionType.SUPPORT_ZONE),
                (~values["first_move_player"], RegionType.CHARACTER_ALL),
                (~values["first_move_player"], RegionType.COMBAT_STATUS_ZONE),
            ]
        return values

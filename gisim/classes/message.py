"""Message classes for communication and calculation
"""

from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from .entity import Entity
from .enums import (
    CardType,
    CharacterPosition,
    ElementType,
    MsgPriority,
    PlayerID,
    RegionType,
)


class Message(Entity, BaseModel, ABC):
    """Abstract base class of different kinds of messages"""

    sender_id: PlayerID
    priority: MsgPriority
    remaining_respondent_zone: list[tuple[PlayerID, RegionType]] = []
    """The message will travel all listed zones for respond. """
    responded_entities: list[UUID] = []
    """The UUID of all responded entities"""
    # @abstractmethod
    # def encode(self):
    #     ...

    def __lt__(self, other: "Message"):
        return self.priority < other.priority


class MessageReceiver(ABC):
    """Abstract base class of different kinds of message receivers"""

    @abstractmethod
    def on_message(self, msg: Message):
        ...


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


class ChangeActivePlayerMsg(Message):
    """Send from Skill/ChangeCharacter"""

    priority: MsgPriority = MsgPriority.GAME_STATUS
    pass


# Player action related.
# After player agent submits an `Action`, `game.judge_action`` will first check its validity
# then convert the action to the corresponding message.


class ChangeCardsMsg(Message):
    """Send from Agent/Card/Support/...
    Include both discard cards and drawing cards."""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    discard_cards_idx: list[int]
    draw_cards_type: list[CardType]
    """If no type specified, use `CardType.ANY`"""
    pass


class RollDiceMsg(Message):
    """Send from Card"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    dice_idx: list[int]
    pass


class ChangeCharacterMsg(Message):
    """Send from Agent/Character(Skill, Elemental Reaction)"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    position: CharacterPosition
    pass


class UseCardMsg(Message):
    """Send from Agent"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    card_idx: int
    card_target: list[tuple[PlayerID, CharacterPosition]]
    pass


class UseSkillMsg(Message):
    """Send from Agent"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    user_position: CharacterPosition
    skill_name: str
    skill_target: list[tuple[PlayerID, CharacterPosition]]
    """In case one character can assign multiple targets in the future"""

    @property
    def remaining_respondent_zone(self):
        return [
            (self.sender_id, RegionType.HAND),
            (
                self.sender_id,
                RegionType.CHARACTER_ZONE,
            ),  # the card may not be used by the active character (e.g. 刻晴的雷楔)
            (self.sender_id, RegionType.COMBAT_STATUS_ZONE),
            (
                ~self.sender_id,
                RegionType.CHARACTER_ZONE,
            ),  # the damage has not been generated yet
            (~self.sender_id, RegionType.COMBAT_STATUS_ZONE),
            (~self.sender_id, RegionType.SUMMON_ZONE),
            (
                ~self.sender_id,
                RegionType.CHARACTER_ZONE,
            ),  # generate damage and then generate
        ]

    pass


class CardCostMsg(Message):
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    card_idx: int
    card_target: list[tuple[PlayerID, CharacterPosition]]
    simulate: bool = False
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""
    cost: dict[ElementType, int] = {}

    @property
    def remaining_respondent_zone(self):
        return [
            (self.sender_id, RegionType.HAND),
            (
                self.sender_id,
                RegionType.CHARACTER_ZONE,
            ),  # the card may not be used by the active character (e.g. 刻晴的雷楔)
            (self.sender_id, RegionType.COMBAT_STATUS_ZONE),
            (self.sender_id, RegionType.SUPPORT_ZONE),
            (self.sender_id, RegionType.DICE_ZONE),
        ]


class SkillCostMsg(Message):
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    user_position: CharacterPosition
    skill_name: str
    skill_target: list[tuple[PlayerID, CharacterPosition]]
    simulate: bool = False
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""
    cost: dict[ElementType, int] = {}

    @property
    def remaining_respondent_zone(self):
        return [
            (self.sender_id, RegionType.ACTIVE_CHARACTER),
            (self.sender_id, RegionType.COMBAT_STATUS_ZONE),
            (self.sender_id, RegionType.SUPPORT_ZONE),
            (self.sender_id, RegionType.DICE_ZONE),
        ]


class ChangeCharacterCostMsg(Message):
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    position: CharacterPosition
    simulate: bool = False
    """Will not trigger the reduce cost status in the simulate mode, for validity check"""
    cost: dict[ElementType, int] = {}

    @property
    def remaining_respondent_zone(self):
        return [
            (self.sender_id, RegionType.ACTIVE_CHARACTER),
            (self.sender_id, RegionType.COMBAT_STATUS_ZONE),
            (self.sender_id, RegionType.SUPPORT_ZONE),
            (self.sender_id, RegionType.DICE_ZONE),
        ]


# Hp related
# This kind of message is usually responded by a lot of entities, from the current character/summon to its target


class GenerateDamageMsg(Message):
    """Send from Character(Skill)/Character Status/Summon/Combat Status"""

    priority: MsgPriority = MsgPriority.HP_CHANGING
    target: list[tuple[PlayerID, CharacterPosition, ElementType, int]]
    pass


class HurtMsg(Message):
    """Send from Character/Summon who is being attacked and all other effects are already calculated"""

    priority: MsgPriority = MsgPriority.HP_CHANGING
    pass


class RecoverHpMsg(Message):
    """Send from Card/Character(Skill)/Equipment/Support/Summon/..."""

    priority: MsgPriority = MsgPriority.HP_CHANGING
    pass


# Special types


class ElementalReactionEffectMsg(Message):
    """Send from Character(under attack)/Summon"""

    priority: MsgPriority = MsgPriority.ELEMENTAL_REACTION_EFFECT
    pass


class CharacterDiedMsg(Message):
    """Send from Character(under attack)"""

    priority: MsgPriority = MsgPriority.CHARACTER_DIED
    pass


# Entity-related


class GenerateSummonMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    pass


class RemoveSummonMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    pass


class GenerateSupportMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    pass


class GenerateCharacterStatusMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    pass


class GenerateCombatStatusMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    pass


class GenerateEquipmentMsg(Message):
    "Usually generated from Cards"
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    pass

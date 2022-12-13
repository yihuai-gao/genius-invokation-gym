"""Message classes for communication and calculation
"""

from abc import ABC, abstractmethod

from .entity import Entity
from .enums import CardType, CharacterPosition, ElementType, MsgType, PlayerID, MsgPriority
from pydantic import BaseModel


class Message(Entity, BaseModel, ABC):
    """Abstract base class of different kinds of messages"""

    sender_id: PlayerID
    priority: MsgPriority
    message_type: MsgType
    # @abstractmethod
    # def encode(self):
    #     ...

    def __lt__(self, other:'Message'):
        return self.priority < other.priority
        


class MessageReceiver(ABC):
    """Abstract base class of different kinds of message receivers"""

    @abstractmethod
    def on_message(self, msg: Message):
        ...


# Game status related
# A lot of entities will be responded by these messages


class RoundStartMsg(Message):
    """Send from Judge"""
    priority: MsgPriority = MsgPriority.GAME_STATUS
    message_type: MsgType = MsgType.RoundStart
    pass

class RoundEndMsg(Message):
    """Send from Judge"""
    priority: MsgPriority = MsgPriority.GAME_STATUS
    message_type: MsgType = MsgType.RoundEnd
    pass


# Player action related.
# After player agent submits an `Action`, `game.judge` will first check its validity
# then convert the action to the corresponding message.


class ChangeCardsMsg(Message):
    """Send from Agent(through Judge)/Card/Support/...
    Include both discard cards and drawing cards."""
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    message_type: MsgType = MsgType.ChangeCards
    discard_cards_idx: list[int]
    draw_cards_type: list[CardType]
    '''If no type specified, use `CardType.ANY`'''
    pass


class RollDiceMsg(Message):
    """Send from Card"""
    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    message_type: MsgType = MsgType.RollDice
    dice_idx: list[int]
    pass


class ChangeCharacterMsg(Message):
    """Send from Agent(through Judge)/Character(Skill, Elemental Reaction)"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    message_type: MsgType = MsgType.ChangeCharacter
    pass


class UseCardMsg(Message):
    """Send from Agent(through Judge)"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    message_type: MsgType = MsgType.UseCard
    card_idx: int
    card_target: list[tuple[PlayerID, CharacterPosition]] 
    pass


class UseSkillMsg(Message):
    """Send from Agent(through Judge)"""

    priority: MsgPriority = MsgPriority.PLAYER_ACTION
    message_type: MsgType = MsgType.UseSkill
    user_position: CharacterPosition
    skill_name: str
    skill_target: list[tuple[PlayerID, CharacterPosition]] 
    '''In case one character can assign multiple targets in the future'''
    pass


# Hp related
# This kind of message is usually responded by a lot of entities, from the current character/summon to its target


class GenerateDamageMsg(Message):
    """Send from Character(Skill)/Character Status/Summon/Combat Status"""
    priority: MsgPriority = MsgPriority.HP_CHANGING
    message_type: MsgType = MsgType.GenerateDamage
    target: list[tuple[PlayerID, CharacterPosition, ElementType, int]]
    pass


class HurtMsg(Message):
    """Send from Character/Summon who is being attacked and all other effects are already calculated"""

    priority: MsgPriority = MsgPriority.HP_CHANGING
    message_type: MsgType = MsgType.Hurt
    pass


class RecoverHpMsg(Message):
    """Send from Card/Character(Skill)/Equipment/Support/Summon/..."""
    
    priority: MsgPriority = MsgPriority.HP_CHANGING
    message_type: MsgType = MsgType.RecoverHp
    pass

# Special types

class ElementalReactionEffectMsg(Message):
    """Send from Character(under attack)/Summon"""
    priority: MsgPriority = MsgPriority.ELEMENTAL_REACTION_EFFECT
    message_type: MsgType = MsgType.ElementalReactionEffect
    pass


class CharacterDiedMsg(Message):
    """Send from Character(under attack)"""
    priority: MsgPriority = MsgPriority.CHARACTER_DIED
    message_type: MsgType = MsgType.CharacterDied
    pass


# Entity-related


class GenerateSummonMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    message_type: MsgType = MsgType.GenerateSummon
    pass


class RemoveSummonMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    message_type: MsgType = MsgType.RemoveSummon
    pass


class GenerateSupportMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    message_type: MsgType = MsgType.GenerateSupport
    pass


class GenerateCharacterStatusMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    message_type: MsgType = MsgType.GenerateCharacterStatus
    pass


class GenerateCombatStatusMsg(Message):
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    message_type: MsgType = MsgType.GenerateCombatStatus
    pass


class GenerateEquipmentMsg(Message):
    "Usually generated from Cards"
    priority: MsgPriority = MsgPriority.ENTITY_GENERATION
    message_type: MsgType = MsgType.GenerateEquipment
    pass

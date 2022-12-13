"""Message classes for communication and calculation
"""

from abc import ABC, abstractmethod

from .entity import Entity
from .enums import MessageType, PlayerID, MessagePriority
from pydantic import BaseModel


class Message(Entity, BaseModel, ABC):
    """Abstract base class of different kinds of messages"""

    sender_id: PlayerID
    priority: MessagePriority
    message_type: MessageType
    # @abstractmethod
    # def encode(self):
    #     ...


class MessageReceiver(ABC):
    """Abstract base class of different kinds of message receivers"""

    @abstractmethod
    def on_message(self, msg: Message):
        ...


# Game status related
# A lot of entities will be responded by these messages


class RoundStartMsg(Message):
    """Send from Judge"""
    priority: MessagePriority = MessagePriority.GAME_STATUS
    message_type: MessageType = MessageType.RoundStart
    pass

class RoundEndMsg(Message):
    """Send from Judge"""
    priority: MessagePriority = MessagePriority.GAME_STATUS
    message_type: MessageType = MessageType.RoundEnd
    pass


# Player action related.
# After player agent submits an `Action`, `game.judge` will first check its validity
# then convert the action to the corresponding message.


class ChangeCardsMsg(Message):
    """Send from Agent(through Judge)/Card/Support/...
    Include only drawing cards."""
    priority: MessagePriority = MessagePriority.PLAYER_ACTION
    message_type: MessageType = MessageType.ChangeCards
    pass


class RollDiceMsg(Message):
    """Send from Agent(through Judge)/Card"""
    priority: MessagePriority = MessagePriority.PLAYER_ACTION
    message_type: MessageType = MessageType.RollDice
    pass


class ChangeCharacterMsg(Message):
    """Send from Agent(through Judge)/Character(Skill, Elemental Reaction)"""

    priority: MessagePriority = MessagePriority.PLAYER_ACTION
    message_type: MessageType = MessageType.ChangeCharacter
    pass


class UseCardMsg(Message):
    """Send from Agent(through Judge)"""

    priority: MessagePriority = MessagePriority.PLAYER_ACTION
    message_type: MessageType = MessageType.UseCard
    pass


class UseSkillMsg(Message):
    """Send from Agent(through Judge)"""

    priority: MessagePriority = MessagePriority.PLAYER_ACTION
    message_type: MessageType = MessageType.UseSkill
    pass


class ElementalTuningMsg(Message):
    """Send from Agent(through Judge)
    元素调和"""

    priority: MessagePriority = MessagePriority.PLAYER_ACTION
    message_type: MessageType = MessageType.ElementalTuning
    pass


# Hp related
# This kind of message is usually responded by a lot of entities, from the current character/summon to its target


class GenerateDamageMsg(Message):
    """Send from Character(Skill)/Character Status/Summon/Combat Status"""
    priority: MessagePriority = MessagePriority.HP_CHANGING
    message_type: MessageType = MessageType.GenerateDamage
    pass


class HurtMsg(Message):
    """Send from Character/Summon who is being attacked and all other effects are already calculated"""

    priority: MessagePriority = MessagePriority.HP_CHANGING
    message_type: MessageType = MessageType.Hurt
    pass


class RecoverHpMsg(Message):
    """Send from Card/Character(Skill)/Equipment/Support/Summon/..."""
    
    priority: MessagePriority = MessagePriority.HP_CHANGING
    message_type: MessageType = MessageType.RecoverHp
    pass

# Special types

class ElementalReactionEffectMsg(Message):
    """Send from Character(under attack)/Summon"""
    priority: MessagePriority = MessagePriority.ELEMENTAL_REACTION_EFFECT
    message_type: MessageType = MessageType.ElementalReactionEffect
    pass


class CharacterDiedMsg(Message):
    """Send from Character(under attack)"""
    priority: MessagePriority = MessagePriority.CHARACTER_DIED
    message_type: MessageType = MessageType.CharacterDied
    pass


# Entity-related


class GenerateSummonMsg(Message):
    priority: MessagePriority = MessagePriority.ENTITY_GENERATION
    message_type: MessageType = MessageType.GenerateSummon
    pass


class RemoveSummonMsg(Message):
    priority: MessagePriority = MessagePriority.ENTITY_GENERATION
    message_type: MessageType = MessageType.RemoveSummon
    pass


class GenerateSupportMsg(Message):
    priority: MessagePriority = MessagePriority.ENTITY_GENERATION
    message_type: MessageType = MessageType.GenerateSupport
    pass


class GenerateCharacterStatusMsg(Message):
    priority: MessagePriority = MessagePriority.ENTITY_GENERATION
    message_type: MessageType = MessageType.GenerateCharacterStatus
    pass


class GenerateCombatStatusMsg(Message):
    priority: MessagePriority = MessagePriority.ENTITY_GENERATION
    message_type: MessageType = MessageType.GenerateCombatStatus
    pass


class GenerateEquipmentMsg(Message):
    "Usually generated from Cards"
    priority: MessagePriority = MessagePriority.ENTITY_GENERATION
    message_type: MessageType = MessageType.GenerateEquipment
    pass

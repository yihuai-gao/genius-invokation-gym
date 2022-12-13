"""Message classes for communication and calculation
"""

from abc import ABC, abstractmethod

from .entity import Entity
from .enums import PlayerID


class Message(Entity, ABC):
    """Abstract base class of different kinds of messages"""

    def __init__(self, sender_id: PlayerID, priority: int):
        self.sender_id = sender_id
        self.priority = priority

    @abstractmethod
    def encode(self):
        ...


class MessageReceiver(ABC):
    """Abstract base class of different kinds of message receivers"""

    @abstractmethod
    def on_message(self, msg: Message):
        ...


# Game status related
# A lot of entities will be responded by these messages


class RoundStartMsg(Message):
    """Send from Judge"""

    pass


class RoundEndMsg(Message):
    """Send from Judge"""

    pass


# Player action related.
# After player agent submits an `Action`, `game.judge` will first check its validity
# then convert the action to the corresponding message.


class ChangeCardsMsg(Message):
    """Send from Agent(through Judge)/Card/Support/...
    Include only drawing cards."""

    pass


class RollDiceMsg(Message):
    """Send from Agent(through Judge)/Card"""

    pass


class ChangeCharacterMsg(Message):
    """Send from Agent(through Judge)/Character(Skill, Elemental Reaction)"""

    pass


class UseCardMsg(Message):
    """Send from Agent(through Judge)"""

    pass


class UseSkillMsg(Message):
    """Send from Agent(through Judge)"""

    pass


class ElementTuningMsg(Message):
    """Send from Agent(through Judge)
    元素调和"""

    pass


# Hp related
# This kind of message is usually responded by a lot of entities, from the current character/summon to its target


class GenerateDamageMsg(Message):
    """Send from Character(Skill)/Character Status/Summon/Combat Status"""

    pass


class HurtMsg(Message):
    """Send from Character/Summon who is being attacked and all other effects are already calculated"""

    pass


class RecoverHpMsg(Message):
    """Send from Card/Character(Skill)/Equipment/Support/Summon/..."""

    def __init__(self, sender_id: PlayerID, priority: int, hp: int):
        super().__init__(sender_id, priority)
        self.hp = hp


class ElementalReactionMsg(Message):
    """Send from Character(under attack)/Summon"""

    pass


class CharacterDiedMsg(Message):
    """Send from Character(under attack)"""

    pass


# Entity-related


class GenerateSummonMsg(Message):
    pass


class RemoveSummonMsg(Message):
    pass


class GenerateSupportMsg(Message):
    pass


class GenerateCharacterStatusMsg(Message):
    pass


class GenerateCombatStatusMsg(Message):
    pass


class GenerateEquipmentMsg(Message):
    "Usually generated from Cards"
    pass

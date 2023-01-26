from abc import ABC, abstractmethod
from collections import OrderedDict
from logging import Logger, getLogger
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .entity import Entity
from .enums import CharPos, PlayerID


class CharacterStatusEntity(Entity, ABC):
    """Status which is attached to a fixed character.
    Shown in the upper line of the character card. Will be calculated earlier."""

    player_id: PlayerID
    position: CharPos
    name: str
    description: str
    active: bool
    remaining_round: int
    value: int

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))


class CombatStatusEntity(Entity, ABC):
    """Status which is attached dynamically to the active character.
    Shown in the lower line of the character card. Will be calculated later."""

    player_id: PlayerID
    position: CharPos = CharPos.ACTIVE
    name: str
    description: str
    active: bool
    remaining_round: int
    value: int

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))

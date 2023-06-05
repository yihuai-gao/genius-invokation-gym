from abc import ABC, abstractmethod
from collections import OrderedDict
from logging import Logger, getLogger
from queue import PriorityQueue
from typing import cast

from gisim.classes.entity import Entity
from gisim.classes.enums import CharPos, PlayerID, StatusType


class CharacterStatusEntity(Entity, ABC):
    """Status which is attached to a fixed character.
    Shown in the upper line of the character card. Will be calculated earlier."""

    player_id: PlayerID
    status_type: StatusType
    position: CharPos
    name: str
    description: str
    active: bool
    remaining_round: int
    remaining_usage: int
    value: int

    def msg_handler(self, msg_queue: PriorityQueue):
        ...

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))


class CombatStatusEntity(Entity, ABC):
    """Status which is attached dynamically to the active character.
    Shown in the lower line of the character card. Will be calculated later."""

    player_id: PlayerID
    # position: CharPos = CharPos.ACTIVE
    name: str
    description: str
    active: bool
    remaining_usage: int
    remaining_round: int
    value: int

    def msg_handler(self, msg_queue: PriorityQueue):
        ...

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))

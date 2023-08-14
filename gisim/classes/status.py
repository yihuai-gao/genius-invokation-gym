from abc import ABC, abstractmethod
from collections import OrderedDict
from logging import Logger, getLogger
from queue import PriorityQueue
from typing import cast

from gisim.classes.entity import Entity
from gisim.classes.enums import CharPos, ElementType, PlayerID
from gisim.env import INF_INT


class CharacterStatusEntity(Entity, ABC):
    """Status which is attached to a fixed character.
    Shown in the upper line of the character card. Will be calculated earlier."""

    player_id: PlayerID
    position: CharPos
    # id: int
    name: str
    description: str
    active: bool
    remaining_round: int
    """E.g. Razor's "The Wolf Within" has 2 remaining rounds. 雷泽q技能附属状态有2回合"""
    remaining_usage: int
    """E.g. Yoimiya's "Niwabi Enshou" has 2 remaining usages. 宵宫e技能状态有2次使用机会"""
    value: int
    """Passive skills of Raiden Shogun, Cyno, Jadeplume Terrorshroom (aka 鸡哥), etc."""
    

    def msg_handler(self, msg_queue: PriorityQueue):
        ...

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))


class CombatStatusEntity(Entity, ABC):
    """Status which is attached dynamically to the active character.
    Shown in the lower line of the character card. Will be calculated later."""

    player_id: PlayerID
    # position: CharPos = CharPos.ACTIVE
    # id: int
    name: str
    description: str
    active: bool
    remaining_round: int
    """E.g. Yoimiya's "Ryuukin Saxifrage" has 2 remaining rounds. 宵宫q技能附属状态有2回合剩余"""
    remaining_usage: int
    """E.g. Shenhe's "Icy Quill" has 3 remaining usages. 申鹤e技能状态有3次使用机会"""
    value: int
    """Some kinds of Shield (as combat status)"""

    def msg_handler(self, msg_queue: PriorityQueue):
        ...

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))

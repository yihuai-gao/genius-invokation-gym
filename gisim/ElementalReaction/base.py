from queue import PriorityQueue
from typing import TYPE_CHECKING, List

from pydantic import BaseModel, validator

from gisim.classes.enums import *

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Reaction(BaseModel):
    """元素反应"""
    id: int
    name: str
    reaction_type: ElementType
    increased_bonuses: int = 0
    """反应的（对伤害）增益:本伤害+2"""

    def to_reaction(self, msg_queue: PriorityQueue, player_id: PlayerID, parent: "CharacterEntity"):
        """反应产生的其他效果，如添加召唤物、添加角色状态、添加阵营出战状态、
        后台角色元素攻击、后台角色穿透伤害等"""
        ...

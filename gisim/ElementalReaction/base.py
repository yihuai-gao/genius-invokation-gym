from queue import PriorityQueue
from typing import TYPE_CHECKING, List, cast

from pydantic import BaseModel, validator

from gisim.classes.enums import *
from gisim.classes.message import (
    ElementalReactionTriggeredMsg,
    DealDamageMsg,
    GenerateSummonMsg,
    GenerateCharacterStatusMsg,
    GenerateCombatStatusMsg,
)


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

    status_name: str = ""
    """为角色附加的效果，冻结"""
    status_remaining_round: int = 0
    status_remaining_usage: int = 0

    combat_status_name: str = ""
    """为阵营附加的效果 草原核 激化领域"""
    combat_status_remaining_round: int = 0
    combat_status_remaining_usage: int = 0

    piercing_damage_value: int = 0

    summon_name: str = ""
    """生成的召唤物"""

    def to_reaction(self, msg_queue: PriorityQueue, parent: "CharacterEntity"):
        msg = msg_queue.get()
        # print(msg)
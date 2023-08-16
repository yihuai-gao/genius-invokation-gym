"""凝光"""
from typing import Dict, List
from queue import PriorityQueue

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    CharPos,
    ElementType,
    EntityType,
    EquipmentType,
    Nation,
    PlayerID,
    SkillType,
    WeaponType,
)
from gisim.classes.status import CombatStatusEntity
from gisim.classes.summon import AttackSummon, Summon


class SparklingScatter(GenericSkill):
    """
    千金掷
    ~~~~~~
    造成1点`岩元素伤害`。
    """

    id: int = 16011
    name: str = "Sparkling Scatter"
    text: str = """
    Deals 1 Geo DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.GEO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.Geo
    damage_value: int = 1


class JadeScreen(GenericSkill):
    """
    璇玑屏
    ~~~~~~
    造成2点`岩元素伤害`，生成`璇玑屏`。
    """

    id: int = 16012
    name: str = "Jade Screen"
    text: str = """
    Deals 2 Geo DMG, creates 1 Jade Screen.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.GEO: 3}
    damage_element: ElementType = ElementType.GEO
    damage_value: int = 2
    combat_status_name: str = "Jade Screen"
    combat_status_id: int = 116011


class Starshatter(GenericSkill):
    """
    天权崩玉
    ~~~~~~~~
    造成6点`岩元素伤害`；如果`璇玑屏`在场，就使此伤害+2。
    """

    id: int = 16013
    name: str = "Starshatter"
    text: str = """
    Deals 6 Geo DMG. If Jade Screen is on the field, deals +2 DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.GEO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.GEO
    damage_value: int = 6


class JadeScreenStatus(CombatStatusEntity):
    """
    Jade Screen
    ~~~~~~
    `战斗行动`Jade Screen
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    id: int = 116011
    name: str = "Jade Screen"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Ningguang(CharacterCard):
    """凝光"""

    id: int = 1601
    name: str = "Ningguang"
    element_type: ElementType = ElementType.GEO
    nations: List[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CATALYST
    skills: List[CharacterSkill] = [
        SparklingScatter(),
        JadeScreen(),
        Starshatter(),
    ]

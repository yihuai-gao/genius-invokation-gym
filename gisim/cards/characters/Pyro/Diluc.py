"""迪卢克"""
from queue import PriorityQueue
from typing import Dict, List

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


class TemperedSword(GenericSkill):
    """
    淬炼之剑
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 13011
    name: str = "Tempered Sword"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.PYRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class SearingOnslaught(GenericSkill):
    """
    逆焰之刃
    ~~~~~~~~
    造成3点`火元素伤害`。每回合第三次使用本技能时，伤害+2。
    """

    id: int = 13012
    name: str = "Searing Onslaught"
    text: str = """
    Deals 3 Pyro DMG. For the third use of this Skill each Round, deals +2 DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.PYRO: 3}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 3


class Dawn(GenericSkill):
    """
    黎明
    ~~~~
    造成8点`火元素伤害`，本角色附属`火元素附魔`。
    """

    id: int = 13013
    name: str = "Dawn"
    text: str = """
    Deals 8 Pyro DMG. This character gains Pyro Infusion.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.PYRO: 4, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 8


class Diluc(CharacterCard):
    """迪卢克"""

    id: int = 1301
    name: str = "Diluc"
    element_type: ElementType = ElementType.PYRO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: List[CharacterSkill] = [
        TemperedSword(),
        SearingOnslaught(),
        Dawn(),
    ]

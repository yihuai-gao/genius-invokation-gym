"""翠翎恐蕈"""
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


class MajesticDance(GenericSkill):
    """
    菌王舞步
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 27011
    name: str = "Majestic Dance"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.DENDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class VolatileSporeCloud(GenericSkill):
    """
    不稳定孢子云
    ~~~~~~~~~~~~
    造成3点`草元素伤害`。
    """

    id: int = 27012
    name: str = "Volatile Spore Cloud"
    text: str = """
    Deals 3 Dendro DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 3


class FeatherSpreading(GenericSkill):
    """
    尾羽豪放
    ~~~~~~~~
    造成4点`草元素伤害`，消耗所有`活化激能`层数，每层使此伤害+1。
    """

    id: int = 27013
    name: str = "Feather Spreading"
    text: str = """
    Deals 4 Dendro DMG, then consumes all Radical Vitality stacks. For each stack consumed, this instance deals +1 DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 4


class RadicalVitality(GenericSkill):
    """
    活化激能
    ~~~~~~~~
    【被动】战斗开始时，初始附属`活化激能`。
    """

    id: int = 27014
    name: str = "Radical Vitality"
    text: str = """
    (Passive) When the battle begins, this character gains Radical Vitality.
    """
    type: SkillType = SkillType.PASSIVE_SKILL
    costs: dict[ElementType, int] = {}


class JadeplumeTerrorshroom(CharacterCard):
    """翠翎恐蕈"""

    id: int = 2701
    name: str = "Jadeplume Terrorshroom"
    element_type: ElementType = ElementType.DENDRO
    nations: list[Nation] = [Nation.Monster]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: list[CharacterSkill] = [
        MajesticDance(),
        VolatileSporeCloud(),
        FeatherSpreading(),
        RadicalVitality(),
    ]

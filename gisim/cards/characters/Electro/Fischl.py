"""菲谢尔"""
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


class BoltsofDownfall(GenericSkill):
    """
    罪灭之矢
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 14011
    name: str = "Bolts of Downfall"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class Nightrider(GenericSkill):
    """
    夜巡影翼
    ~~~~~~~~
    造成1点`雷元素伤害`，召唤`奥兹`。
    """

    id: int = 14012
    name: str = "Nightrider"
    text: str = """
    Deals 1 Electro DMG, summons 1 Oz.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ELECTRO, 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 1
    summon_name: str = "Oz"


class MidnightPhantasmagoria(GenericSkill):
    """
    至夜幻现
    ~~~~~~~~
    造成4点`雷元素伤害`，对所有敌方后台角色造成2点``穿透伤害``。
    """

    id: int = 14013
    name: str = "Midnight Phantasmagoria"
    text: str = """
    Deals 4 Electro DMG, deals 2 Piercing DMG to all opposing characters on standby.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 4
    piercing_damage_value: int = 2


class SummonOz(AttackSummon):
    """
    Oz
    ~~~~~~
    `召唤物`Oz
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    name: str = "Oz"


class Fischl(CharacterCard):
    """菲谢尔"""

    id: int = 1401
    name: str = "Fischl"
    element_type: ElementType = ElementType.ELECTRO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.BOW
    skills: list[CharacterSkill] = [
        BoltsofDownfall(),
        Nightrider(),
        MidnightPhantasmagoria(),
    ]

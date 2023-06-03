"""琴"""
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
from gisim.classes.summon import AttackSummon, Summon
from gisim.classes.status import CombatStatusEntity

class FavoniusBladework(GenericSkill):
    """
    西风剑术
    ~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 15021
    name: str = "Favonius Bladework"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class GaleBlade(GenericSkill):
    """
    风压剑
    ~~~~~~
    造成3点`风元素伤害`，使对方强制切换到下一个角色。
    """
    id: int = 15022
    name: str = "Gale Blade"
    text: str = """
    Deals 3 Anemo DMG, the target is forcibly switched to the next character.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 3


class DandelionBreeze(GenericSkill):
    """
    蒲公英之风
    ~~~~~~~~~~
    治疗所有我方角色2点，召唤`蒲公英领域`。
    """
    id: int = 15023
    name: str = "Dandelion Breeze"
    text: str = """
    Heals all your characters for 2 HP, summons 1 Dandelion Field.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ANEMO: 4, ElementType.POWER: 3}
    summon_name: str = "Dandelion Field"


class SummonDandelionField(AttackSummon):
    """
    Dandelion Field
    ~~~~~~
    `召唤物`Dandelion Field
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Dandelion Field"


class Jean(CharacterCard):
    """琴"""
    id: int = 1502
    name: str = "Jean"
    element_type: ElementType = ElementType.ANEMO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.SWORD
    skills: list[CharacterSkill] = [
        FavoniusBladework(),
        GaleBlade(),
        DandelionBreeze(),
    ]


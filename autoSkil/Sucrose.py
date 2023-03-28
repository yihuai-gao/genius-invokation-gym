"""砂糖"""
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

class WindSpiritCreation(GenericSkill):
    """
    简式风灵作成
    ~~~~~~~~~~~~
    造成1点`风元素伤害`。
    """
    id: int = 15011
    name: str = "Wind Spirit Creation"
    text: str = """
    Deals 1 Anemo DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ANEMO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Anemo
    damage_value: int = 1


class AstableAnemohypostasisCreation(GenericSkill):
    """
    风灵作成·陆叁零捌
    ~~~~~~~~~~~~~~~~~~
    造成3点`风元素伤害`，使对方强制切换到前一个角色。
    """
    id: int = 15012
    name: str = "Astable Anemohypostasis Creation - 6308"
    text: str = """
    Deals 3 Anemo DMG, the target is forcibly switched to the previous character.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ANEMO, 3}
    damage_element: ElementType = ElementType.Anemo
    damage_value: int = 3


class ForbiddenCreationIsomerTypeII(GenericSkill):
    """
    禁·风灵作成·柒伍同构贰型
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    造成1点`风元素伤害`，召唤`大型风灵`。
    """
    id: int = 15013
    name: str = "Forbidden Creation - Isomer 75 / Type II"
    text: str = """
    Deals 1 Anemo DMG, summons 1 Large Wind Spirit.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ANEMO, 3, ElementType.POWER, 2}
    damage_element: ElementType = ElementType.Anemo
    damage_value: int = 1
    summon_name: str = "Large Wind Spirit"


class SummonLargeWindSpirit(AttackSummon):
    """
    Large Wind Spirit
    ~~~~~~
    `召唤物`Large Wind Spirit
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Large Wind Spirit"


class Sucrose(CharacterCard):
    """砂糖"""
    id: int = 1501
    name: str = "Sucrose"
    element_type: ElementType = ElementType.ANEMO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.CATALYST
    skills: list[CharacterSkill] = [
        WindSpiritCreation(),
        AstableAnemohypostasisCreation(),
        ForbiddenCreationIsomerTypeII(),
    ]


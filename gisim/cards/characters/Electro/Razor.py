"""雷泽"""
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


class SteelFang(GenericSkill):
    """
    钢脊
    ~~~~
    造成2点`物理伤害`。
    """

    id: int = 14021
    name: str = "Steel Fang"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class ClawandThunder(GenericSkill):
    """
    利爪与苍雷
    ~~~~~~~~~~
    造成3点`雷元素伤害`。
    """

    id: int = 14022
    name: str = "Claw and Thunder"
    text: str = """
    Deals 3 Electro DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 3


class LightningFang(GenericSkill):
    """
    雷牙
    ~~~~
    造成5点`雷元素伤害`，本角色附属`雷狼`。
    """

    id: int = 14023
    name: str = "Lightning Fang"
    text: str = """
    Deals 5 Electro DMG. This character gains The Wolf Within.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 5


class Razor(CharacterCard):
    """雷泽"""

    id: int = 1402
    name: str = "Razor"
    element_type: ElementType = ElementType.ELECTRO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: list[CharacterSkill] = [
        SteelFang(),
        ClawandThunder(),
        LightningFang(),
    ]

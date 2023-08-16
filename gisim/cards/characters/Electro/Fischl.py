"""菲谢尔"""
from typing import Dict, List

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.summon import AttackSummon


class BoltsofDownfall(GenericSkill):
    """Normal Attack: Bolts of Downfall
    Deals 2 Physical DMG."""

    id: int = 14011
    name: str = "Bolts of Downfall"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class Nightrider(GenericSkill):
    """Elemental Skill: Nightrider
    Deals 1 Electro DMG, summons 1 Oz."""

    id: int = 14012
    name: str = "Nightrider"
    text: str = """
    Deals 1 Electro DMG, summons 1 Oz.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 1
    summon_name: str = "Oz"
    summon_id: int = 114011


class MidnightPhantasmagoria(GenericSkill):
    """Elemental Burst: Midnight Phantasmagoria
    Deals 4 Electro DMG, deals 2 Piercing DMG to all opposing characters on standby."""

    id: int = 14013
    name: str = "Midnight Phantasmagoria"
    text: str = """
    Deals 4 Electro DMG, deals 2 Piercing DMG to all opposing characters on standby.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 4
    piercing_damage_value: int = 2


class Oz(AttackSummon):
    """Summon: Oz
    End Phase: Deal 1 Electro DMG.
    Usage(s): 2"""

    id: int = 114011
    name: str = "Oz"
    usages: int = 2
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 1


class Fischl(CharacterCard):
    """菲谢尔"""

    id: int = 1401
    name: str = "Fischl"
    element_type: ElementType = ElementType.ELECTRO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.BOW
    skills: List[CharacterSkill] = [
        BoltsofDownfall(),
        Nightrider(),
        MidnightPhantasmagoria(),
    ]

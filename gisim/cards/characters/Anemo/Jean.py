"""Jean"""
from typing import Dict, List

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.summon import AttackSummon


class FavoniusBladework(GenericSkill):
    """
    Normal Attack: Favonius Bladework
    Deals 2 Physical DMG.
    """

    id: int = 15021
    name: str = "Favonius Bladework"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class GaleBlade(GenericSkill):
    """Elemental Skill: Gale Blade
    Deals 3 Anemo DMG, the target is forcibly switched to the next character.
    """

    id: int = 15022
    name: str = "Gale Blade"
    text: str = """
    Deals 3 Anemo DMG, the target is forcibly switched to the next character.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 3
    # TODO: forcibly switched to the next character


class DandelionBreeze(CharacterSkill):
    """Elemental Burst: Dandelion Breeze
    Heals all your characters for 2 HP, summons 1 Dandelion Field.
    """

    id: int = 15023
    name: str = "Dandelion Breeze"
    text: str = """
    Heals all your characters for 2 HP, summons 1 Dandelion Field.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 4, ElementType.POWER: 3}
    heal_all_value: int = 2
    summon_name: str = "Dandelion Field"
    summon_id: int = 115021


class DandelionField(AttackSummon):
    """
    Summon: Dandelion Field
    End Phase: Deal 2 Anemo DMG, heal your active character for 1 HP.
    Usage(s): 2
    """

    id: int = 115021
    name: str = "Dandelion Field"
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 1
    usages: int = 2


class Jean(CharacterCard):
    """Jean"""

    id: int = 1502
    name: str = "Jean"
    element_type: ElementType = ElementType.ANEMO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.SWORD
    skills: List[CharacterSkill] = [
        FavoniusBladework(),
        GaleBlade(),
        DandelionBreeze(),
    ]

"""Sucrose"""
from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    ElementType,
    Nation,
    SkillType,
    WeaponType,
)
from gisim.classes.summon import AttackSummon
class WindSpiritCreation(GenericSkill):
    """Normal Attack: Wind Spirit Creation
    Deals 1 Anemo DMG."""
    id: int = 15011
    name: str = "Wind Spirit Creation"
    text: str = """
    Deals 1 Anemo DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 1


class AstableAnemohypostasisCreation6308(GenericSkill):
    """Elemental Skill: Astable Anemohypostasis Creation - 6308
    Deals 3 Anemo DMG, the target is forcibly switched to the previous character."""
    id: int = 15012
    name: str = "Astable Anemohypostasis Creation 6308"
    text: str = """
    Deals 3 Anemo DMG, the target is forcibly switched to the previous character.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 3


class ForbiddenCreationIsomer75TypeII(GenericSkill):
    """Elemental Burst: Forbidden Creation - Isomer 75 / Type II
    Deals 1 Anemo DMG, summons 1 Large Wind Spirit."""
    id: int = 15013
    name: str = "Forbidden Creation Isomer 75  Type II"
    text: str = """
    Deals 1 Anemo DMG, summons 1 Large Wind Spirit.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 1
    summon_name: str = "Large Wind Spirit"


class LargeWindSpirit(AttackSummon):
    """Summon: Large Wind Spirit
    End Phase: Deal 2 Anemo DMG.
    Usage(s): 3
    After your character or Summon triggers a Swirl reaction: Convert the Elemental Type of this card and change its DMG dealt to the element Swirled. (Can only be converted once before leaving the field)
    """
    name: str = "Large Wind Spirit"


class Sucrose(CharacterCard):
    """Sucrose"""
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
        AstableAnemohypostasisCreation6308(),
        ForbiddenCreationIsomer75TypeII(),
    ]


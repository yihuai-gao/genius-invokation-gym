"""Eula"""
from queue import PriorityQueue
from typing import cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, StatusType, WeaponType
from gisim.classes.message import DealDamageMsg
from gisim.classes.summon import AttackSummon
from gisim.classes.status import CharacterStatusEntity


class FavoniusBladeworkEdel(GenericSkill):
    """Normal Attack: Favonius Bladework - Edel
    Deals 2 Physical DMG."""

    id: int = 61761
    name: str = "Favonius Bladework Edel"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2


class IcetideVortex(GenericSkill):
    """Elemental Skill: Icetide Vortex
    Deals 2 Physical DMG."""

    id: int = 61762
    name: str = "Icetide Vortex"
    text: str = """Deals 2 Cryo DMG. If this character has not yet gained Grimheart, they will gain Grimheart."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2


class Grimheart(CharacterStatusEntity):
    name: str = "Grimheart"
    element: ElementType = ElementType.CRYO
    status_type: StatusType = StatusType.ATTACK_BUFF
    description: str = """After the character to which this is attached uses Icetide Vortex: Remove this status, DMG +2 for this instance."""
    value: int = 0
    active: bool = True


class BaneofAllEvil(GenericSkill):
    """Elemental Burst: Glacial Illumination
    Deals 2 Cryo DMG, summons 1 Lightfall Sword."""

    id: int = 65623
    name: str = "Glacial Illumination"
    text: str = """Deals 2 Cryo DMG, summons 1 Lightfall Sword."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 4


class LightfallSword(AttackSummon):
    """Summon: Lightfall Sword
    When Eula uses a Normal Attack or Elemental Skill, this card will accumulate 2 Zeal stacks, but Eula will not gain Energy.
    End Phase: Discard this card and deal 2 Physical DMG.
    Each Zeal stack adds 1 DMG to this damage instance.
    (Effects on this card's Usage will apply to Zeal.)"""

    name: str = "Lightfall Sword"


class Eula(CharacterCard):
    """Eula"""

    id: int = 6176
    name: str = "Eula"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: list[CharacterSkill] = [
        FavoniusBladeworkEdel(),
        IcetideVortex(),
        BaneofAllEvil(),
    ]

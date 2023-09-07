"""丘丘岩盔王"""
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


class PlamaLawa(GenericSkill):
    """
    Plama Lawa
    ~~~~~~~~~~~~~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 26011
    name: str = "Plama Lawa"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.GEO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class MovoLawa(GenericSkill):
    """
    Movo Lawa
    ~~~~~~~~~~~~~~~~~~
    造成3点`物理伤害`。
    """

    id: int = 26012
    name: str = "Movo Lawa"
    text: str = """
    Deals 3 Physical DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.GEO: 3}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 3


class UpaShato(GenericSkill):
    """
    Upa Shato
    ~~~~~~~~~~~~~~~~~~
    造成5点`物理伤害`。
    """

    id: int = 26013
    name: str = "Upa Shato"
    text: str = """
    Deals 5 Physical DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.GEO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 5


class InfusedStonehide(GenericSkill):
    """
    魔化：岩盔
    ~~~~~~~~~~
    【被动】战斗开始时，初始附属`岩盔`和`坚岩之力`。
    """

    id: int = 26014
    name: str = "Infused Stonehide"
    text: str = """
    (Passive) When the battle begins, this character gains Stonehide and Stone Force.
    """
    type: SkillType = SkillType.PASSIVE_SKILL
    costs: Dict[ElementType, int] = {}


class StonehideLawachurl(CharacterCard):
    """丘丘岩盔王"""

    id: int = 2601
    name: str = "Stonehide Lawachurl"
    element_type: ElementType = ElementType.GEO
    nations: List[Nation] = [Nation.Monster, Nation.Hilichurl]
    health_point: int = 8
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: List[CharacterSkill] = [
        PlamaLawa(),
        MovoLawa(),
        UpaShato(),
        InfusedStonehide(),
    ]

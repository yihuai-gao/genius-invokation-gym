"""Chongyun"""
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
from gisim.env import INF_INT


class Demonbane(GenericSkill):
    """Normal Attack: Demonbane
    Deals 2 Physical DMG."""

    id: int = 11041
    name: str = "Demonbane"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class ChonghuasLayeredFrost(GenericSkill):
    """Elemental Skill: Chonghua's Layered Frost
    Deals 3 Cryo DMG, creates 1 Chonghua Frost Field."""

    id: int = 11042
    name: str = "Chonghuas Layered Frost"
    text: str = """Deals 3 Cryo DMG, creates 1 Chonghua Frost Field."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 3
    combat_status_name: str = "Chonghuas Frost Field"
    combat_status_id: int = 111041

    """Chonghua's Frost Field
Your Sword, Claymore, and Polearm-wielding characters' Physical DMG is converted to Cryo DMG.
Duration (Rounds): 2
    """


class CloudPartingStar(GenericSkill):
    """Elemental Burst: Cloud Parting Star
    Deals 7 Cryo DMG."""

    id: int = 11043
    name: str = "Cloud Parting Star"
    text: str = """Deals 7 Cryo DMG."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 7


class Chongyun(CharacterCard):
    """Chongyun"""

    id: int = 1104
    name: str = "Chongyun"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: list[CharacterSkill] = [
        Demonbane(),
        ChonghuasLayeredFrost(),
        CloudPartingStar(),
    ]


class ChonghuasFrostFieldStatus(CombatStatusEntity):
    """Combat Status: Chonghua's Frost Field
    Your Sword, Claymore, and Polearm-wielding characters' Physical DMG is converted to Cryo DMG.
    Duration (Rounds): 2
    """

    id: int = 111041
    name: str = "Chonghuas Frost Field"
    description: str = """Your Sword, Claymore, and Polearm-wielding characters' Physical DMG is converted to Cryo DMG.Duration (Rounds): 2"""
    active: bool = True
    value: int = 0
    remaining_round: int = 2
    remaining_usage: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        # TODO: Get Sword, Claymore, Polearm-wielding Character.
        return False

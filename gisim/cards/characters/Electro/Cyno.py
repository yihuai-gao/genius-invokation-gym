"""赛诺"""
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


class InvokersSpear(GenericSkill):
    """
    七圣枪术
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 14041
    name: str = "Invoker's Spear"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class SecretRiteChasmicSoulfarer(GenericSkill):
    """
    秘仪·律渊渡魂
    ~~~~~~~~~~~~~~
    造成3点`雷元素伤害`。
    """

    id: int = 14042
    name: str = "Secret Rite: Chasmic Soulfarer"
    text: str = """
    Deals 3 Electro DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 3


class SacredRiteWolfsSwiftness(GenericSkill):
    """
    圣仪·煟煌随狼行
    ~~~~~~~~~~~~~~~~
    造成4点`雷元素伤害`，\n`启途誓使`的[凭依]级数+2。
    """

    id: int = 14043
    name: str = "Sacred Rite: Wolf's Swiftness"
    text: str = """
    Deals 4 Electro DMG.\nPactsworn Pathclearer's Indwelling Level +2.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 4, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 4


class LawfulEnforcer(GenericSkill):
    """
    行度誓惩
    ~~~~~~~~
    【被动】战斗开始时，初始附属`启途誓使`。
    """

    id: int = 14044
    name: str = "Lawful Enforcer"
    text: str = """
    (Passive) When the battle begins, this character gains Pactsworn Pathclearer.
    """
    type: SkillType = SkillType.PASSIVE_SKILL
    costs: Dict[ElementType, int] = {}


class Cyno(CharacterCard):
    """赛诺"""

    id: int = 1404
    name: str = "Cyno"
    element_type: ElementType = ElementType.ELECTRO
    nations: List[Nation] = [Nation.Sumeru]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.POLEARM
    skills: List[CharacterSkill] = [
        InvokersSpear(),
        SecretRiteChasmicSoulfarer(),
        SacredRiteWolfsSwiftness(),
        LawfulEnforcer(),
    ]

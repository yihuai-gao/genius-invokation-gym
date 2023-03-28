"""愚人众·火之债务处理人"""
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

class Thrust(GenericSkill):
    """
    突刺
    ~~~~
    造成2点`物理伤害`。
    """
    id: int = 23011
    name: str = "Thrust"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.PYRO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Physical
    damage_value: int = 2


class Prowl(GenericSkill):
    """
    伺机而动
    ~~~~~~~~
    造成1点`火元素伤害`，本角色附属`潜行`。
    """
    id: int = 23012
    name: str = "Prowl"
    text: str = """
    Deals 1 Pyro DMG. This character gains Stealth.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.PYRO, 3}
    damage_element: ElementType = ElementType.Pyro
    damage_value: int = 1


class BladeAblaze(GenericSkill):
    """
    焚毁之锋
    ~~~~~~~~
    造成5点`火元素伤害`。
    """
    id: int = 23013
    name: str = "Blade Ablaze"
    text: str = """
    Deals 5 Pyro DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.PYRO, 3, ElementType.POWER, 2}
    damage_element: ElementType = ElementType.Pyro
    damage_value: int = 5


class StealthMaster(GenericSkill):
    """
    潜行大师
    ~~~~~~~~
    【被动】战斗开始时，初始附属`潜行`。
    """
    id: int = 23014
    name: str = "Stealth Master"
    text: str = """
    (Passive) When the battle begins, this character gains Stealth.
    """
    type: SkillType = SkillType.PASSIVE_SKILL
    costs: dict[ElementType, int] = {}


class FatuiPyroAgent(CharacterCard):
    """愚人众·火之债务处理人"""
    id: int = 2301
    name: str = "Fatui Pyro Agent"
    element_type: ElementType = ElementType.PYRO
    nations: list[Nation] = [Nation.Fatui]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: list[CharacterSkill] = [
        Thrust(),
        Prowl(),
        BladeAblaze(),
        StealthMaster(),
    ]


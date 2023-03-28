"""愚人众·藏镜仕女"""
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

class WaterBall(GenericSkill):
    """
    水弹
    ~~~~
    造成1点`水元素伤害`。
    """
    id: int = 22021
    name: str = "Water Ball"
    text: str = """
    Deals 1 Hydro DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.HYDRO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Hydro
    damage_value: int = 1


class InfluxBlast(GenericSkill):
    """
    潋波绽破
    ~~~~~~~~
    造成3点`水元素伤害`，目标角色附属`水光破镜`。
    """
    id: int = 22022
    name: str = "Influx Blast"
    text: str = """
    Deals 3 Hydro DMG. The target character receives Refraction.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.HYDRO, 3}
    damage_element: ElementType = ElementType.Hydro
    damage_value: int = 3


class RippledReflection(GenericSkill):
    """
    粼镜折光
    ~~~~~~~~
    造成5点`水元素伤害`。
    """
    id: int = 22023
    name: str = "Rippled Reflection"
    text: str = """
    Deals 5 Hydro DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.HYDRO, 3, ElementType.POWER, 2}
    damage_element: ElementType = ElementType.Hydro
    damage_value: int = 5


class MirrorMaiden(CharacterCard):
    """愚人众·藏镜仕女"""
    id: int = 2202
    name: str = "Mirror Maiden"
    element_type: ElementType = ElementType.HYDRO
    nations: list[Nation] = [Nation.Fatui]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: list[CharacterSkill] = [
        WaterBall(),
        InfluxBlast(),
        RippledReflection(),
    ]


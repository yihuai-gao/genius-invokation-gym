"""诺艾尔"""
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

class FavoniusBladeworkMaid(GenericSkill):
    """
    西风剑术·女仆
    ~~~~~~~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 16021
    name: str = "Favonius Bladework - Maid"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.GEO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Physical
    damage_value: int = 2


class Breastplate(GenericSkill):
    """
    护心铠
    ~~~~~~
    造成1点`岩元素伤害`，生成`护体岩铠`。
    """
    id: int = 16022
    name: str = "Breastplate"
    text: str = """
    Deals 1 Geo DMG, creates 1 Full Plate.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.GEO, 3}
    damage_element: ElementType = ElementType.Geo
    damage_value: int = 1
    combat_status_name: str = "Full Plate"


class SweepingTime(GenericSkill):
    """
    大扫除
    ~~~~~~
    造成4点`岩元素伤害`，本角色附属`大扫除`。
    """
    id: int = 16023
    name: str = "Sweeping Time"
    text: str = """
    Deals 4 Geo DMG. This character gains Sweeping Time.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.GEO, 4, ElementType.POWER, 2}
    damage_element: ElementType = ElementType.Geo
    damage_value: int = 4


class CombatStatuFullPlate(CombatStatusEntity):
    """
    Full Plate
    ~~~~~~
    `战斗行动`Full Plate
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Full Plate"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Noelle(CharacterCard):
    """诺艾尔"""
    id: int = 1602
    name: str = "Noelle"
    element_type: ElementType = ElementType.GEO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: list[CharacterSkill] = [
        FavoniusBladeworkMaid(),
        Breastplate(),
        SweepingTime(),
    ]


"""甘雨"""
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

class LiutianArchery(GenericSkill):
    """
    流天射术
    ~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 11011
    name: str = "Liutian Archery"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Physical
    damage_value: int = 2


class TrailoftheQilin(GenericSkill):
    """
    山泽麟迹
    ~~~~~~~~
    造成1点`冰元素伤害`，生成`冰莲`。
    """
    id: int = 11012
    name: str = "Trail of the Qilin"
    text: str = """
    Deals 1 Cryo DMG, creates 1 Ice Lotus.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO, 3}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 1
    combat_status_name: str = "Ice Lotus"


class FrostflakeArrow(GenericSkill):
    """
    霜华矢
    ~~~~~~
    造成2点`冰元素伤害`，对所有敌方后台角色造成`2点`穿透伤害``。
    """
    id: int = 11013
    name: str = "Frostflake Arrow"
    text: str = """
    Deals 2 Cryo DMG, deals 2 Piercing DMG to all opposing characters on standby.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO, 5}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 2
    piercing_damage_value: int = 2


class CelestialShower(GenericSkill):
    """
    降众天华
    ~~~~~~~~
    造成1点`冰元素伤害`，对所有敌方后台角色造成`1点`穿透伤害``，召唤`冰灵珠`。
    """
    id: int = 11014
    name: str = "Celestial Shower"
    text: str = """
    Deals 1 Cryo DMG, deals 1 Piercing DMG to all opposing characters on standby, summons 1 Sacred Cryo Pearl.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO, 3, ElementType.POWER, 2}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 1
    piercing_damage_value: int = 1
    summon_name: str = "Sacred Cryo Pearl"


class CombatStatuIceLotus(CombatStatusEntity):
    """
    Ice Lotus
    ~~~~~~
    `战斗行动`Ice Lotus
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Ice Lotus"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class SummonSacredCryoPearl(AttackSummon):
    """
    Sacred Cryo Pearl
    ~~~~~~
    `召唤物`Sacred Cryo Pearl
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Sacred Cryo Pearl"


class Ganyu(CharacterCard):
    """甘雨"""
    id: int = 1101
    name: str = "Ganyu"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.BOW
    skills: list[CharacterSkill] = [
        LiutianArchery(),
        TrailoftheQilin(),
        FrostflakeArrow(),
        CelestialShower(),
    ]


"""甘雨"""
import logging
from queue import PriorityQueue
from typing import TYPE_CHECKING, Dict, List

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.status import CombatStatusEntity
from gisim.classes.summon import AttackSummon

if TYPE_CHECKING:
    pass


class LiutianArchery(GenericSkill):
    """
    流天射术
    ~~~~~~~~
    `普通攻击` 造成2点`物理伤害`。
    """

    id: int = 11011
    name: str = "Liutian Archery"
    text: str = """
    Deals 2 Physical DMG.
    """
    costs: Dict[ElementType, int] = {ElementType.CRYO: 1, ElementType.ANY: 2}
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class FrostflakeArrow(GenericSkill):
    """
    霜华矢
    ~~~~~
    `普通攻击` 造成2点`冰元素伤害`，对所有敌方`后台角色`造成2点`穿透伤害`。
    """

    id: int = 11013
    name: str = "Frostflake Arrow"
    text: str = """
    Deals 2 Cryo DMG, deals 2 Piercing DMG to all opposing characters on standby.
    """
    costs: Dict[ElementType, int] = {ElementType.CRYO: 5}
    type: SkillType = SkillType.NORMAL_ATTACK
    piercing_damage_value: int = 2

    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2


class TrailoftheQilin(GenericSkill):
    """
    山泽麟迹
    ~~~~~~~
    `元素战技`造成1点`冰元素伤害`，生成`冰莲`。
    """

    id: int = 11012
    name: str = "Trail of the Qilin"
    text: str = """
    Deals 1 Cryo DMG, creates 1 Ice Lotus.
    """

    costs: Dict[ElementType, int] = {ElementType.CRYO: 3}
    type: SkillType = SkillType.ELEMENTAL_SKILL

    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 1

    combat_status_name: str = "Ice Lotus"
    combat_status_id: int = 111012


class IceLotusStatus(CombatStatusEntity):
    """
    冰莲
    ~~~
    `战斗行动`给出战角色 添加一个护盾 盾值为1，最多可以使用2次
    """

    id: int = 111012
    name: str = "Ice Lotus"
    description: str = "给出战角色 添加一个护盾 盾值为1，最多可以使用2次。"
    value: int = 2

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        logging.info(top_msg)
        return True


class CelestialShower(GenericSkill):
    """
    降众天华
    ~~~~~~~
    `元素爆发`造成1点`冰元素伤害`，对所有敌方`后台角色`造成1点`穿透伤害`，召唤`冰灵珠`。
    """

    id: int = 11014
    name: str = "Celestial Shower"
    text: str = """
    Deals 1 Cryo DMG, deals 1 Piercing DMG to all opposing characters on standby, summons 1 Sacred Cryo Pearl.
    """
    costs: Dict[ElementType, int] = {ElementType.CRYO: 3, ElementType.POWER: 2}
    type: SkillType = SkillType.ELEMENTAL_BURST
    piercing_damage_value: int = 1
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 1
    summon_name: str = "Sacred Cryo Pearl"
    summon_id: int = 111011


class SacredCryoPearl(AttackSummon):
    """
    冰灵珠
    ~~~~~
    `召唤物`在结束阶段造成1点`冰元素伤害`，对所有`后台角色`造成1点`穿透伤害`，该召唤物可以被使用2次。
    """

    id: int = 111011
    name: str = "Sacred Cryo Pearl"
    usages: int = 2
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 1
    piercing_damage_value: int = 1


class Ganyu(CharacterCard):
    """甘雨"""

    id: int = 1101
    name: str = "Ganyu"
    element_type: ElementType = ElementType.CRYO
    nations: List[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.BOW
    skills: List[CharacterSkill] = [
        LiutianArchery(),
        FrostflakeArrow(),
        TrailoftheQilin(),
        CelestialShower(),
    ]

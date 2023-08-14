"""香菱"""
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


class DoughFu(GenericSkill):
    """
    白案功夫
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 13021
    name: str = "Dough-Fu"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.PYRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class GuobaAttack(GenericSkill):
    """
    锅巴出击
    ~~~~~~~~
    召唤`锅巴`。
    """

    id: int = 13022
    name: str = "Guoba Attack"
    text: str = """
    Summons 1 Guoba.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.PYRO: 3}
    summon_name: str = "Guoba"
    summon_id: int = 113021


class Pyronado(GenericSkill):
    """
    旋火轮
    ~~~~~~
    造成2点`火元素伤害`，生成`旋火轮`。
    """

    id: int = 13023
    name: str = "Pyronado"
    text: str = """
    Deals 2 Pyro DMG, creates 1 Pyronado.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.PYRO: 4, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 2
    combat_status_name: str = "Pyronado"
    combat_status_id: int = 113022


class Guoba(AttackSummon):
    """
    Guoba
    ~~~~~~
    `召唤物`Guoba
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    id: int = 113021
    name: str = "Guoba"


class PyronadoStatus(CombatStatusEntity):
    """
    Pyronado
    ~~~~~~
    `战斗行动`Pyronado
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    id: int = 113022
    name: str = "Pyronado"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Xiangling(CharacterCard):
    """香菱"""

    id: int = 1302
    name: str = "Xiangling"
    element_type: ElementType = ElementType.PYRO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.POLEARM
    skills: list[CharacterSkill] = [
        DoughFu(),
        GuobaAttack(),
        Pyronado(),
    ]

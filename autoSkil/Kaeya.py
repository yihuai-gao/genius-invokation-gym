"""凯亚"""
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

class CeremonialBladework(GenericSkill):
    """
    仪典剑术
    ~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 11031
    name: str = "Ceremonial Bladework"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Physical
    damage_value: int = 2


class Frostgnaw(GenericSkill):
    """
    霜袭
    ~~~~
    造成3点`冰元素伤害`。
    """
    id: int = 11032
    name: str = "Frostgnaw"
    text: str = """
    Deals 3 Cryo DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO, 3}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 3


class GlacialWaltz(GenericSkill):
    """
    凛冽轮舞
    ~~~~~~~~
    造成1点`冰元素伤害`，生成`寒冰之棱`。
    """
    id: int = 11033
    name: str = "Glacial Waltz"
    text: str = """
    Deals 1 Cryo DMG, creates 1 Icicle.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO, 4, ElementType.POWER, 2}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 1
    combat_status_name: str = "Icicle"


class CombatStatuIcicle(CombatStatusEntity):
    """
    Icicle
    ~~~~~~
    `战斗行动`Icicle
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Icicle"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Kaeya(CharacterCard):
    """凯亚"""
    id: int = 1103
    name: str = "Kaeya"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.SWORD
    skills: list[CharacterSkill] = [
        CeremonialBladework(),
        Frostgnaw(),
        GlacialWaltz(),
    ]


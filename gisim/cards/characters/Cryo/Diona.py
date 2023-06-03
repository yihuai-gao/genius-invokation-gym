"""迪奥娜"""
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

class KtzleinStyle(GenericSkill):
    """
    猎人射术
    ~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 11021
    name: str = "Kätzlein Style"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class IcyPaws(GenericSkill):
    """
    猫爪冻冻
    ~~~~~~~~
    造成2点`冰元素伤害`，生成`猫爪护盾`。
    """
    id: int = 11022
    name: str = "Icy Paws"
    text: str = """
    Deals 2 Cryo DMG, creates 1 Cat-Claw Shield.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2
    combat_status_name: str = "Cat-Claw Shield"


class SignatureMix(GenericSkill):
    """
    最烈特调
    ~~~~~~~~
    造成1点`冰元素伤害`，治疗此角色2点，召唤`酒雾领域`。
    """
    id: int = 11023
    name: str = "Signature Mix"
    text: str = """
    Deals 1 Cryo DMG, heals this character for 2 HP, summons 1 Drunken Mist.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 1
    summon_name: str = "Drunken Mist"


class CombatStatuCatClawShield(CombatStatusEntity):
    """
    Cat-Claw Shield
    ~~~~~~
    `战斗行动`Cat-Claw Shield
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Cat-Claw Shield"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class SummonDrunkenMist(AttackSummon):
    """
    Drunken Mist
    ~~~~~~
    `召唤物`Drunken Mist
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Drunken Mist"


class Diona(CharacterCard):
    """迪奥娜"""
    id: int = 1102
    name: str = "Diona"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.BOW
    skills: list[CharacterSkill] = [
        KtzleinStyle(),
        IcyPaws(),
        SignatureMix(),
    ]


"""班尼特"""
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


class StrikeofFortune(GenericSkill):
    """
    好运剑
    ~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 13031
    name: str = "Strike of Fortune"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.PYRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class PassionOverload(GenericSkill):
    """
    热情过载
    ~~~~~~~~
    造成3点`火元素伤害`。
    """

    id: int = 13032
    name: str = "Passion Overload"
    text: str = """
    Deals 3 Pyro DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.PYRO: 3}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 3


class FantasticVoyage(GenericSkill):
    """
    美妙旅程
    ~~~~~~~~
    造成2点`火元素伤害`，生成`鼓舞领域`。
    """

    id: int = 13033
    name: str = "Fantastic Voyage"
    text: str = """
    Deals 2 Pyro DMG, creates 1 Inspiration Field.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.PYRO: 4, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 2
    combat_status_name: str = "Inspiration Field"
    combat_status_id: int = 113031


class InspirationFieldStatus(CombatStatusEntity):
    """
    Inspiration Field
    ~~~~~~
    `战斗行动`Inspiration Field
    """

    id: int = 113031
    name: str = "Inspiration Field"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Bennett(CharacterCard):
    """班尼特"""

    id: int = 1303
    name: str = "Bennett"
    element_type: ElementType = ElementType.PYRO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.SWORD
    skills: List[CharacterSkill] = [
        StrikeofFortune(),
        PassionOverload(),
        FantasticVoyage(),
    ]

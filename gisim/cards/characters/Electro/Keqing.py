"""刻晴"""
from typing import Dict, List
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


class YunlaiSwordsmanship(GenericSkill):
    """
    云来剑法
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 14031
    name: str = "Yunlai Swordsmanship"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class StellarRestoration(GenericSkill):
    """
    星斗归位
    ~~~~~~~~
    造成3点`雷元素伤害`，生成手牌`雷楔`。
    """

    id: int = 14032
    name: str = "Stellar Restoration"
    text: str = """
    Deals 3 Electro DMG, creates 1 Lightning Stiletto.
    """
    # TODO: 生成雷楔牌，而非状态
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 3
    combat_status_name: str = "Lightning Stiletto"


class StarwardSword(GenericSkill):
    """
    天街巡游
    ~~~~~~~~
    造成4点`雷元素伤害`，对所有敌方后台角色造成`3点`穿透伤害``。
    """

    id: int = 14033
    name: str = "Starward Sword"
    text: str = """
    Deals 4 Electro DMG, deals 3 Piercing DMG to all opposing characters on standby.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 4, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 4
    piercing_damage_value: int = 3


class LightningStilettoStatus(CombatStatusEntity):
    """
    Lightning Stiletto
    ~~~~~~
    `战斗行动`Lightning Stiletto
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    name: str = "Lightning Stiletto"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Keqing(CharacterCard):
    """刻晴"""

    id: int = 1403
    name: str = "Keqing"
    element_type: ElementType = ElementType.ELECTRO
    nations: List[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.SWORD
    skills: List[CharacterSkill] = [
        YunlaiSwordsmanship(),
        StellarRestoration(),
        StarwardSword(),
    ]

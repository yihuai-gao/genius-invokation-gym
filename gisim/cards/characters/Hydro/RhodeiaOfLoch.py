"""纯水精灵·洛蒂娅"""
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


class Surge(GenericSkill):
    """
    翻涌
    ~~~~
    造成1点`水元素伤害`。
    """

    id: int = 22011
    name: str = "Surge"
    text: str = """
    Deals 1 Hydro DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.HYDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 1


class OceanidMimicSummoning(GenericSkill):
    """
    纯水幻造
    ~~~~~~~~
    随机召唤1种`纯水幻形`。（优先生成不同的类型）
    """

    id: int = 22012
    name: str = "Oceanid Mimic Summoning"
    text: str = """
    Randomly summons 1 Oceanid Mimic (Prioritizes summoning a different type from preexisting ones).
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.HYDRO: 3}


class TheMyriadWilds(GenericSkill):
    """
    林野百态
    ~~~~~~~~
    随机召唤2种`纯水幻形`。（优先生成不同的类型）
    """

    id: int = 22013
    name: str = "The Myriad Wilds"
    text: str = """
    Randomly summons 2 Oceanid Mimic (Prioritizes summoning different types).
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.HYDRO: 5}


class TideandTorrent(GenericSkill):
    """
    潮涌与激流
    ~~~~~~~~~~
    造成2点`水元素伤害`；我方每有1个召唤物，再使此伤害+2。
    """

    id: int = 22014
    name: str = "Tide and Torrent"
    text: str = """
    Deals 2 Hydro DMG. For each friendly Summon on the field, deals +2 additional DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.HYDRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 2


class RhodeiaOfLoch(CharacterCard):
    """纯水精灵·洛蒂娅"""

    id: int = 2201
    name: str = "Rhodeia of Loch"
    element_type: ElementType = ElementType.HYDRO
    nations: List[Nation] = [Nation.Monster]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: List[CharacterSkill] = [
        Surge(),
        OceanidMimicSummoning(),
        TheMyriadWilds(),
        TideandTorrent(),
    ]

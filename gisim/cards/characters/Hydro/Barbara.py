"""芭芭拉"""
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


class WhisperofWater(GenericSkill):
    """
    水之浅唱
    ~~~~~~~~
    造成1点`水元素伤害`。
    """

    id: int = 12011
    name: str = "Whisper of Water"
    text: str = """
    Deals 1 Hydro DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.HYDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 1


class LettheShowBegin(GenericSkill):
    """
    演唱，开始♪
    ~~~~~~~~~~~~
    造成1点`水元素伤害`，召唤`歌声之环`。
    """

    id: int = 12012
    name: str = "Let the Show Begin♪"
    text: str = """
    Deals 1 Hydro DMG, summons 1 Melody Loop.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.HYDRO: 3}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 1
    summon_name: str = "Melody Loop"
    summon_id: int = 112011


class ShiningMiracle(GenericSkill):
    """
    闪耀奇迹♪
    ~~~~~~~~~~
    治疗所有我方角色4点。
    """

    id: int = 12013
    name: str = "Shining Miracle♪"
    text: str = """
    Heals all of your characters for 4 HP.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.HYDRO: 3, ElementType.POWER: 3}


class MelodyLoop(AttackSummon):
    """
    Melody Loop
    ~~~~~~
    `召唤物`Melody Loop
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    id: int = 112011
    name: str = "Melody Loop"


class Barbara(CharacterCard):
    """芭芭拉"""

    id: int = 1201
    name: str = "Barbara"
    element_type: ElementType = ElementType.HYDRO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CATALYST
    skills: List[CharacterSkill] = [
        WhisperofWater(),
        LettheShowBegin(),
        ShiningMiracle(),
    ]

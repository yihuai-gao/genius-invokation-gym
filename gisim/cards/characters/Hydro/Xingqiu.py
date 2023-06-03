"""行秋"""
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


class GuhuaStyle(GenericSkill):
    """
    古华剑法
    ~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 12021
    name: str = "Guhua Style"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.HYDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class FatalRainscreen(GenericSkill):
    """
    画雨笼山
    ~~~~~~~~
    造成2点`水元素伤害`，本角色`附着水元素`，生成`雨帘剑`。
    """
    id: int = 12022
    name: str = "Fatal Rainscreen"
    text: str = """
    Deals 2 Hydro DMG, grants this character Hydro Application, creates 1 Rain Sword.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.HYDRO: 3}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 2
    combat_status_name: str = "Rain Sword"


class Raincutter(GenericSkill):
    """
    裁雨留虹
    ~~~~~~~~
    造成1点`水元素伤害`，本角色`附着水元素`，生成`虹剑势`。
    """
    id: int = 12023
    name: str = "Raincutter"
    text: str = """
    Deals 1 Hydro DMG, grants this character Hydro Application, creates 1 Rainbow Bladework.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.HYDRO:3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 1
    combat_status_name: str = "Rainbow Bladework"



class Xingqiu(CharacterCard):
    """行秋"""
    id: int = 1202
    name: str = "Xingqiu"
    element_type: ElementType = ElementType.HYDRO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.SWORD
    skills: list[CharacterSkill] = [
        GuhuaStyle(),
        FatalRainscreen(),
        Raincutter(),
    ]

"""魔偶剑鬼"""
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

class Ichimonji(GenericSkill):
    """
    一文字
    ~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 25011
    name: str = "Ichimonji"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class BlusteringBlade(GenericSkill):
    """
    孤风刀势
    ~~~~~~~~
    召唤`剑影·孤风`。
    """
    id: int = 25012
    name: str = "Blustering Blade"
    text: str = """
    Summons 1 Shadowsword: Lone Gale.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3}
    summon_name: str = "Shadowsword: Lone Gale"


class FrostyAssault(GenericSkill):
    """
    霜驰影突
    ~~~~~~~~
    召唤`剑影·霜驰`。
    """
    id: int = 25013
    name: str = "Frosty Assault"
    text: str = """
    Summons 1 Shadowsword: Galloping Frost.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    summon_name: str = "Shadowsword: Galloping Frost"


class PseudoTenguSweeper(GenericSkill):
    """
    机巧伪天狗抄
    ~~~~~~~~~~~~
    造成4点`风元素伤害`，触发所有我方`剑影`召唤物的效果。（不消耗其可用次数）
    """
    id: int = 25014
    name: str = "Pseudo Tengu Sweeper"
    text: str = """
    Deals 4 Anemo DMG, triggers the effect(s) of all your Shadowsword Summon(s). (Does not consume their Usages)
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 4


class SummonShadowswordLoneGale(AttackSummon):
    """
    Shadowsword: Lone Gale
    ~~~~~~
    `召唤物`Shadowsword: Lone Gale
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Shadowsword: Lone Gale"


class SummonShadowswordGallopingFrost(AttackSummon):
    """
    Shadowsword: Galloping Frost
    ~~~~~~
    `召唤物`Shadowsword: Galloping Frost
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Shadowsword: Galloping Frost"


class MaguuKenki(CharacterCard):
    """魔偶剑鬼"""
    id: int = 2501
    name: str = "Maguu Kenki"
    element_type: ElementType = ElementType.ANEMO
    nations: list[Nation] = [Nation.Monster]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: list[CharacterSkill] = [
        Ichimonji(),
        BlusteringBlade(),
        FrostyAssault(),
        PseudoTenguSweeper(),
    ]


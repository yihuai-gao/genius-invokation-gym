"""柯莱"""
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

class SupplicantsBowmanship(GenericSkill):
    """
    祈颂射艺
    ~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 17011
    name: str = "Supplicant's Bowmanship"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.DENDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class FloralBrush(GenericSkill):
    """
    拂花偈叶
    ~~~~~~~~
    造成3点`草元素伤害`。
    """
    id: int = 17012
    name: str = "Floral Brush"
    text: str = """
    Deals 3 Dendro DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 3


class TrumpCardKitty(GenericSkill):
    """
    猫猫秘宝
    ~~~~~~~~
    造成2点`草元素伤害`，召唤`柯里安巴`。
    """
    id: int = 17013
    name: str = "Trump-Card Kitty"
    text: str = """
    Deals 2 Dendro DMG, summons 1 Cuilein-Anbar.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 2
    summon_name: str = "Cuilein-Anbar"


class SummonCuileinAnbar(AttackSummon):
    """
    Cuilein-Anbar
    ~~~~~~
    `召唤物`Cuilein-Anbar
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Cuilein-Anbar"


class Collei(CharacterCard):
    """柯莱"""
    id: int = 1701
    name: str = "Collei"
    element_type: ElementType = ElementType.DENDRO
    nations: list[Nation] = [Nation.Sumeru]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.BOW
    skills: list[CharacterSkill] = [
        SupplicantsBowmanship(),
        FloralBrush(),
        TrumpCardKitty(),
    ]


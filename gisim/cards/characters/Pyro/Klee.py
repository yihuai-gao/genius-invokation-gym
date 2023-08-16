"""可莉"""
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


class Kaboom(GenericSkill):
    """
    砰砰
    ~~~~
    造成1点`火元素伤害`。
    """

    id: int = 13061
    name: str = "Kaboom!"
    text: str = """
    Deals 1 Pyro DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.PYRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 1


class JumpyDumpty(GenericSkill):
    """
    蹦蹦炸弹
    ~~~~~~~~
    造成3点`火元素伤害`，本角色附属`爆裂火花`。
    """

    id: int = 13062
    name: str = "Jumpy Dumpty"
    text: str = """
    Deals 3 Pyro DMG. This character gains Explosive Spark.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.PYRO: 3}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 3


class SparksnSplash(GenericSkill):
    """
    轰轰火花
    ~~~~~~~~
    造成3点`火元素伤害`，在对方场上生成`轰轰火花`。
    """

    id: int = 13063
    name: str = "Sparks 'n' Splash"
    text: str = """
    Deals 3 Pyro DMG, creates 1 Sparks 'n' Splash at the opponent's play area.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.PYRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 3


class Klee(CharacterCard):
    """可莉"""

    id: int = 1306
    name: str = "Klee"
    element_type: ElementType = ElementType.PYRO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CATALYST
    skills: List[CharacterSkill] = [
        Kaboom(),
        JumpyDumpty(),
        SparksnSplash(),
    ]

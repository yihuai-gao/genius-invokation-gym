"""雷泽"""
from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType


class SteelFang(GenericSkill):
    """Normal Attack: Steel Fang
    Deals 2 Physical DMG.
    """

    id: int = 14021
    name: str = "Steel Fang"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class ClawandThunder(GenericSkill):
    """Elemental Skill: Claw and Thunder
    Deals 3 Electro DMG.
    """

    id: int = 14022
    name: str = "Claw and Thunder"
    text: str = """Deals 3 Electro DMG."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 3


class LightningFang(GenericSkill):
    """Elemental Burst: Lightning Fang
    Deals 5 Electro DMG. This character gains The Wolf Within."""

    id: int = 14023
    name: str = "Lightning Fang"
    text: str = """Deals 5 Electro DMG. This character gains The Wolf Within."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ELECTRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 5
    status_name: str = "The Wolf Within"
    status_remaining_round: int = 2


class Razor(CharacterCard):
    """Razor"""

    id: int = 1402
    name: str = "Razor"
    element_type: ElementType = ElementType.ELECTRO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: list[CharacterSkill] = [
        SteelFang(),
        ClawandThunder(),
        LightningFang(),
    ]

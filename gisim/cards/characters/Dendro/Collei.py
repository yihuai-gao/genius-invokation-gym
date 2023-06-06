"""柯莱"""
from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.summon import AttackSummon


class SupplicantsBowmanship(GenericSkill):
    """Normal Attack: Supplicant's Bowmanship
    Deals 2 Physical DMG.
    """

    id: int = 17011
    name: str = "Supplicants Bowmanship"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.DENDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class FloralBrush(GenericSkill):
    """Elemental Skill: Floral Brush
    Deals 3 Dendro DMG.
    """

    id: int = 17012
    name: str = "Floral Brush"
    text: str = """Deals 3 Dendro DMG."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 3


class TrumpCardKitty(GenericSkill):
    """Elemental Burst: Trump-Card Kitty
    Deals 2 Dendro DMG, summons 1 Cuilein-Anbar.
    """

    id: int = 17013
    name: str = "Trump Card Kitty"
    text: str = """Deals 2 Dendro DMG, summons 1 Cuilein-Anbar."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 2
    summon_name: str = "Cuilein Anbar"


class CuileinAnbar(AttackSummon):
    """Summon: Cuilein Anbar
    End Phase: Deal 2 Dendro DMG.Usage(s): 2
    """

    name: str = "Cuilein Anbar"
    usages: int = 2
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 2


class Collei(CharacterCard):
    """Collei"""

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

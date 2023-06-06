from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.summon import AttackSummon


class Akara(GenericSkill):
    """Normal Attack: Akara
    Deals 1 Dendro DMG.
    """

    id: int = 65641
    name: str = "Akara"
    text: str = """Deals 1 Dendro DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.DENDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 1


class AllSchemestoKnow(GenericSkill):
    """Elemental Skill: All Schemes to Know
    Deals 2 Dendro DMG, applies the Seed of Skandha to target character. 
    If the target character already has Seed of Skandha applied to them, 
    then apply Seed of Skandha to all opposing characters instead."""

    id: int = 65642
    name: str = "All Schemes to Know"
    text: str = """Deals 2 Dendro DMG, applies the Seed of Skandha to target character. If the target character already has Seed of Skandha applied to them, then apply Seed of Skandha to all opposing characters instead."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 2


class AllSchemestoKnowTathata(GenericSkill):
    """Elemental Skill: All Schemes to Know: Tathata
    Deals 3 Dendro DMG, applies the Seed of Skandha to all opposing characters."""

    id: int = 65643
    name: str = "All Schemes to Know Tathata"
    text: str = """Deals 3 Dendro DMG, applies the Seed of Skandha to all opposing characters."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.DENDRO: 5}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 3
    
class IllusoryHeart(GenericSkill):
    """Elemental Burst: Illusory Heart
    Deals 4 Dendro DMG. creates 1 Shrine of Maya."""

    id: int = 65644
    name: str = "Illusory Heart"
    text: str = """Deals 4 Dendro DMG. creates 1 Shrine of Maya."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3,ElementType.POWER: 2}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 4


class Nahida(CharacterCard):
    """Nahida"""

    id: int = 6564
    name: str = "Nahida"
    element_type: ElementType = ElementType.DENDRO
    nations: list[Nation] = [Nation.Sumeru]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CATALYST
    skills: list[CharacterSkill] = [
        Akara(),
        AllSchemestoKnow(),
        AllSchemestoKnowTathata(),
        IllusoryHeart()
        
    ]

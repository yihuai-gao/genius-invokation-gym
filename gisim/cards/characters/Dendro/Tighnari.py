from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.summon import AttackSummon


class KhandaBarrierBuster(GenericSkill):
    """Normal Attack: Khanda Barrier-Buster
    Deals 2 Physical DMG.
    """

    id: int = 63211
    name: str = "Khanda Barrier Buster"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.DENDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 2


class VijnanaPhalaMine(GenericSkill):
    """Elemental Skill: Vijnana-Phala Mine
    Deals 2 Dendro DMG. This character gains Vijana Suffusion."""

    id: int = 63212
    name: str = "Vijnana Phala Mine"
    text: str = """Deals 2 Dendro DMG. This character gains Vijana Suffusion."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 2


class VijanaSuffusion(AttackSummon):
    """Summon: Vijana Suffusion
    End Phase: Deal 1 Dendro DMG.
    (Can stack. Max 2 stacks.)
    Usage(s): 1
    """

    name: str = "Vijana Suffusion"
    usages: int = 2
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 2


class FashionersTanglevineShaft(GenericSkill):
    """Elemental Burst: Fashioner's Tanglevine Shaft
    Deals 4 Dendro DMG, deals 1 Piercing DMG to all opposing characters on standby."""

    id: int = 63214
    name: str = "Fashioners Tanglevine Shaft"
    text: str = """Deals 4 Dendro DMG, deals 1 Piercing DMG to all opposing characters on standby."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.DENDRO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.DENDRO
    damage_value: int = 4
    piercing_damage_value: int = 1


class Tighnari(CharacterCard):
    """Tighnari"""

    id: int = 6321
    name: str = "Tighnari"
    element_type: ElementType = ElementType.DENDRO
    nations: list[Nation] = [Nation.Sumeru]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.BOW
    skills: list[CharacterSkill] = [
        KhandaBarrierBuster(),
        VijnanaPhalaMine(),
        FashionersTanglevineShaft(),
    ]

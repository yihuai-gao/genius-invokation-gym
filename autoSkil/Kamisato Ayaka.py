"""神里绫华"""
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

class KamisatoArtKabuki(GenericSkill):
    """
    神里流·倾
    ~~~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 11051
    name: str = "Kamisato Art: Kabuki"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Physical
    damage_value: int = 2


class KamisatoArtHyouka(GenericSkill):
    """
    神里流·冰华
    ~~~~~~~~~~~~
    造成3点`冰元素伤害`。
    """
    id: int = 11052
    name: str = "Kamisato Art: Hyouka"
    text: str = """
    Deals 3 Cryo DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO, 3}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 3


class KamisatoArtSoumetsu(GenericSkill):
    """
    神里流·霜灭
    ~~~~~~~~~~~~
    造成4点`冰元素伤害`，召唤`霜见雪关扉`。
    """
    id: int = 11053
    name: str = "Kamisato Art: Soumetsu"
    text: str = """
    Deals 4 Cryo DMG, summons 1 Frostflake Seki no To.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO, 3, ElementType.POWER, 3}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 4
    summon_name: str = "Frostflake Seki no To"


class KamisatoArtSenho(GenericSkill):
    """
    神里流·霰步
    ~~~~~~~~~~~~
    【被动】此角色被切换为「出战角色」时，附属`冰元素附魔`。
    """
    id: int = 11054
    name: str = "Kamisato Art: Senho"
    text: str = """
    (Passive) When switched to be the active character, this character gains Cryo Elemental Infusion.
    """
    type: SkillType = SkillType.PASSIVE_SKILL
    costs: dict[ElementType, int] = {}


class SummonFrostflakeSekinoTo(AttackSummon):
    """
    Frostflake Seki no To
    ~~~~~~
    `召唤物`Frostflake Seki no To
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Frostflake Seki no To"


class KamisatoAyaka(CharacterCard):
    """神里绫华"""
    id: int = 1105
    name: str = "Kamisato Ayaka"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Inazuma]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.SWORD
    skills: list[CharacterSkill] = [
        KamisatoArtKabuki(),
        KamisatoArtHyouka(),
        KamisatoArtSoumetsu(),
        KamisatoArtSenho(),
    ]


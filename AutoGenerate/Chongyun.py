"""重云"""
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

class Demonbane(GenericSkill):
    """
    灭邪四式
    ~~~~~~~~
    造成2点`物理伤害`。
    """
    id: int = 11041
    name: str = "Demonbane"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO, 1, ElementType.ANY, 2}
    damage_element: ElementType = ElementType.Physical
    damage_value: int = 2


class ChonghuasLayeredFrost(GenericSkill):
    """
    重华叠霜
    ~~~~~~~~
    造成3点`冰元素伤害`，生成`重华叠霜领域`。
    """
    id: int = 11042
    name: str = "Chonghua's Layered Frost"
    text: str = """
    Deals 3 Cryo DMG, creates 1 Chonghua Frost Field.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO, 3}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 3
    combat_status_name: str = "Chonghua Frost Field"


class CloudPartingStar(GenericSkill):
    """
    云开星落
    ~~~~~~~~
    造成7点`冰元素伤害`。
    """
    id: int = 11043
    name: str = "Cloud-Parting Star"
    text: str = """
    Deals 7 Cryo DMG.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO, 3, ElementType.POWER, 3}
    damage_element: ElementType = ElementType.Cryo
    damage_value: int = 7


class CombatStatuChonghuaFrostField(CombatStatusEntity):
    """
    Chonghua Frost Field
    ~~~~~~
    `战斗行动`Chonghua Frost Field
    请完善这个类的效果,应该是召唤物或者战斗效果
    """
    name: str = "Chonghua Frost Field"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Chongyun(CharacterCard):
    """重云"""
    id: int = 1104
    name: str = "Chongyun"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: list[CharacterSkill] = [
        Demonbane(),
        ChonghuasLayeredFrost(),
        CloudPartingStar(),
    ]


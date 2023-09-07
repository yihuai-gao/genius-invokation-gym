"""宵宫"""
from queue import PriorityQueue
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
from gisim.classes.status import CharacterStatusEntity, CombatStatusEntity
from gisim.classes.summon import AttackSummon, Summon


class FireworkFlareUp(GenericSkill):
    """
    烟火打扬
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 13051
    name: str = "Firework Flare-Up"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.PYRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class NiwabiFireDance(GenericSkill):
    """
    焰硝庭火舞
    ~~~~~~~~~~
    本角色附属`庭火焰硝`。（此技能不产生充能）
    """

    id: int = 13052
    name: str = "Niwabi Fire-Dance"
    text: str = """
    This character gains Niwabi Enshou. (This Skill does not grant Energy)
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.PYRO: 1}


class RyuukinSaxifrage(GenericSkill):
    """
    琉金云间草
    ~~~~~~~~~~
    造成4点`火元素伤害`，生成`琉金火光`。
    """

    id: int = 13053
    name: str = "Ryuukin Saxifrage"
    text: str = """
    Deals 4 Pyro DMG, creates 1 Aurous Blaze.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.PYRO: 4, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 4
    combat_status_name: str = "Aurous Blaze"
    combat_status_id: int = 113052


class NiwabiEnshouStatus(CharacterStatusEntity):

    id: int = 113051
    name: str = "Niwabi Enshou"


class AurousBlazeStatus(CombatStatusEntity):
    """
    Aurous Blaze
    ~~~~~~
    `战斗行动`Aurous Blaze
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    id: int = 113052
    name: str = "Aurous Blaze"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Yoimiya(CharacterCard):
    """宵宫"""

    id: int = 1305
    name: str = "Yoimiya"
    element_type: ElementType = ElementType.PYRO
    nations: List[Nation] = [Nation.Inazuma]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.BOW
    skills: List[CharacterSkill] = [
        FireworkFlareUp(),
        NiwabiFireDance(),
        RyuukinSaxifrage(),
    ]

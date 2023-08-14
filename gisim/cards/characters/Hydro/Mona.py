"""莫娜"""
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
from gisim.classes.status import CombatStatusEntity
from gisim.classes.summon import AttackSummon, Summon


class RippleofFate(GenericSkill):
    """
    因果点破
    ~~~~~~~~
    造成1点`水元素伤害`。
    """

    id: int = 12031
    name: str = "Ripple of Fate"
    text: str = """
    Deals 1 Hydro DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.HYDRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 1


class MirrorReflectionofDoom(GenericSkill):
    """
    水中幻愿
    ~~~~~~~~
    造成1点`水元素伤害`，召唤`虚影`。
    """

    id: int = 12032
    name: str = "Mirror Reflection of Doom"
    text: str = """
    Deals 1 Hydro DMG, summons 1 Reflection.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.HYDRO: 3}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 1
    summon_name: str = "Reflection"
    summon_id: int = 112031


class StellarisPhantasm(GenericSkill):
    """
    星命定轨
    ~~~~~~~~
    造成4点`水元素伤害`，生成`泡影`。
    """

    id: int = 12033
    name: str = "Stellaris Phantasm"
    text: str = """
    Deals 4 Hydro DMG, creates 1 Illusory Bubble.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.HYDRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.HYDRO
    damage_value: int = 4
    combat_status_name: str = "Illusory Bubble"


class IllusoryTorrent(GenericSkill):
    """
    虚实流动
    ~~~~~~~~
    【被动】`此角色为出战角色，我方执行「切换角色」行动时：`将此次切换视为「`快速行动`」而非「`战斗行动`」。（每回合1次）
    """

    id: int = 12034
    name: str = "Illusory Torrent"
    text: str = """
    (Passive) When you perform "Switch Character" while Mona is your active character: This switch is considered a Fast Action instead of a Combat Action. (Once per Round)
    """
    type: SkillType = SkillType.PASSIVE_SKILL
    costs: dict[ElementType, int] = {}


class Reflection(AttackSummon):
    """
    Reflection
    ~~~~~~
    `召唤物`Reflection
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    id: int = 112031
    name: str = "Reflection"


class CombatStatuIllusoryBubble(CombatStatusEntity):
    """
    Illusory Bubble
    ~~~~~~
    `战斗行动`Illusory Bubble
    请完善这个类的效果,应该是召唤物或者战斗效果
    """

    name: str = "Illusory Bubble"

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        """请编写处理函数"""
        pass


class Mona(CharacterCard):
    """莫娜"""

    id: int = 1203
    name: str = "Mona"
    element_type: ElementType = ElementType.HYDRO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CATALYST
    skills: list[CharacterSkill] = [
        RippleofFate(),
        MirrorReflectionofDoom(),
        StellarisPhantasm(),
        IllusoryTorrent(),
    ]

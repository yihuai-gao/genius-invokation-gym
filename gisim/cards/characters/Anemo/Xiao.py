"""Xiao"""
from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    ElementType,
    Nation,
    SkillType,
    WeaponType,
    StatusType
)
from gisim.classes.summon import AttackSummon
from gisim.status import CombatStatusEntity
from gisim.env import INF_INT
from queue import PriorityQueue
from gisim.classes.message import DealDamageMsg
from typing import cast
from gisim.status import CharacterStatusEntity


class WhirlwindThrust(GenericSkill):
    """Normal Attack: Whirlwind Thrust
    Deals 2 Physical DMG."""
    id: int = 65621
    name: str = "Whirlwind Thrust"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 2


class LemniscaticWindCycling(GenericSkill):
    """Elemental Skill: Lemniscatic Wind Cycling
    Deals 3 Anemo DMG."""
    id: int = 65622
    name: str = "Lemniscatic Wind Cycling"
    text: str = """Deals 3 Anemo DMG."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 3


class BaneofAllEvil(GenericSkill):
    """Elemental Burst: Bane of All Evil
    Deals 4 Anemo DMG. This character gains Yaksha's Mask."""
    id: int = 65623
    name: str = "Bane of All Evil"
    text: str = """Deals 4 Anemo DMG. This character gains Yaksha's Mask."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {
        ElementType.ANEMO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 4


class YakshasMask(CharacterStatusEntity):
    """Character Status: Yaksha's Mask
    The character to which this is attached has their Physical DMG dealt converted to Anemo DMG and they will deal +1 Anemo DMG.
    When the character to which this is attached uses a Plunging Attack: +2 additional DMG.
    If the character this card is attached to is the active character, when you perform "Switch Character": Spend 1 less Elemental Die. (Once per Round)
    Duration (Rounds): 2"""
    name: str = "Yakshas Mask"
    element: ElementType = ElementType.ANEMO
    status_type: StatusType = StatusType.ATTACK_BUFF
    description: str = """The character to which this is attached has their Physical DMG dealt converted to Pyro DMG, and they will deal +1 Pyro DMG.Some times can Apply [Blood Blossom].Duration (Rounds): 2"""
    value: int = 0
    active: bool = True

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return False

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attacker == (self.player_id, self.position):
                updated = True
                for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(top_msg.targets):
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        self.element if element_type is ElementType.NONE else element_type,
                        dmg_val + 1,
                    )
        #TODO:Plunging Attack

        if updated:
            msg_queue.queue[0].responded_entities.append(self._uuid)
        return updated

class Xiao(CharacterCard):
    """Xiao"""
    id: int = 5652
    name: str = "Sucrose"
    element_type: ElementType = ElementType.ANEMO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.POLEARM
    skills: list[CharacterSkill] = [
        WhirlwindThrust(),
        LemniscaticWindCycling(),
        BaneofAllEvil(),
    ]

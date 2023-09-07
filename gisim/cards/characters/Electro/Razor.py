"""雷泽"""
from queue import PriorityQueue
from typing import Dict, List, cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import AttackType, ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import DealDamageMsg, RoundEndMsg
from gisim.classes.status import CharacterStatusEntity, CombatStatusEntity
from gisim.classes.summon import AttackSummon, Summon
from gisim.env import INF_INT


class SteelFang(GenericSkill):
    """Normal Attack: Steel Fang
    Deals 2 Physical DMG.
    """

    id: int = 14021
    name: str = "Steel Fang"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
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
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 3


class LightningFang(GenericSkill):
    """Elemental Burst: Lightning Fang
    Deals 5 Electro DMG. This character gains The Wolf Within."""

    id: int = 14023
    name: str = "Lightning Fang"
    text: str = """Deals 5 Electro DMG. This character gains The Wolf Within."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 5
    status_name: str = "The Wolf Within"
    status_id: int = 114021
    status_remaining_round: int = 2


class Razor(CharacterCard):
    """Razor"""

    id: int = 1402
    name: str = "Razor"
    element_type: ElementType = ElementType.ELECTRO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.CLAYMORE
    skills: List[CharacterSkill] = [
        SteelFang(),
        ClawandThunder(),
        LightningFang(),
    ]


class TheWolfWithinStatus(CharacterStatusEntity):
    """Character Status: The Wolf Within
    After the character to which this is attached uses a Normal Attack or an Elemental Skill:
    Deal 2 Electro DMG.
    Duration (Rounds): 2"""

    id: int = 114021
    name: str = "The Wolf Within"
    element: ElementType = ElementType.ELECTRO
    description: str = """After the character to which this is attached uses a Normal Attack or an Elemental Skill: Deal 2 Electro DMG.Duration (Rounds): 2"""
    value: int = 0
    active: bool = True
    remaining_round: int = 2
    remaining_usage: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return False

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            attacker_id, attacker_pos = top_msg.attacker
            if (
                attacker_id == self.player_id
                and attacker_pos == self.position
                and top_msg.attack_type
                in [AttackType.NORMAL_ATTACK, AttackType.ELEMENTAL_SKILL]
            ):
                new_msg = DealDamageMsg(
                    sender_id=self.player_id,
                    attack_type=AttackType.COMBAT_STATUS,
                    attacker=(self.player_id, self.position),
                    targets=[
                        (target_id, target_pos, self.element, 1)
                        for target_id, target_pos, element_type, dmg_val in top_msg.targets
                    ],
                )
                msg_queue.put(new_msg)
                updated = True

        if isinstance(top_msg, RoundEndMsg):
            self.remaining_round -= 1
            if self.remaining_round == 0:
                self.remaining_usage = 0
                self.active = False

        if updated:
            top_msg.responded_entities.append(self._uuid)

        return updated

"""Sucrose"""
from queue import PriorityQueue
from typing import Dict, List, cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    AttackType,
    CharPos,
    ElementalReactionType,
    ElementType,
    Nation,
    SkillType,
    WeaponType,
)
from gisim.classes.message import (
    DealDamageMsg,
    ElementalReactionTriggeredMsg,
    RoundEndMsg,
)
from gisim.classes.summon import AttackSummon


class WindSpiritCreation(GenericSkill):
    """Normal Attack: Wind Spirit Creation
    Deals 1 Anemo DMG."""

    id: int = 15011
    name: str = "Wind Spirit Creation"
    text: str = """
    Deals 1 Anemo DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 1


class AstableAnemohypostasisCreation6308(GenericSkill):
    """Elemental Skill: Astable Anemohypostasis Creation - 6308
    Deals 3 Anemo DMG, the target is forcibly switched to the previous character."""

    id: int = 15012
    name: str = "Astable Anemohypostasis Creation 6308"
    text: str = """
    Deals 3 Anemo DMG, the target is forcibly switched to the previous character.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 3


class ForbiddenCreationIsomer75TypeII(GenericSkill):
    """Elemental Burst: Forbidden Creation - Isomer 75 / Type II
    Deals 1 Anemo DMG, summons 1 Large Wind Spirit."""

    id: int = 15013
    name: str = "Forbidden Creation Isomer 75 Type II"
    text: str = """
    Deals 1 Anemo DMG, summons 1 Large Wind Spirit.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 1
    summon_name: str = "Large Wind Spirit"
    summon_id: int = 115011


class LargeWindSpirit(AttackSummon):
    """Summon: Large Wind Spirit
    End Phase: Deal 2 Anemo DMG.
    Usage(s): 3
    After your character or Summon triggers a Swirl reaction: Convert the Elemental Type of this card and change its DMG dealt to the element Swirled. (Can only be converted once before leaving the field)
    """

    id: int = 115011
    name: str = "Large Wind Spirit"
    usages: int = 3
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 2
    element_type_change: bool = False

    def msg_handler(self, msg_queue: PriorityQueue):
        msg = msg_queue.queue[0]
        if self._uuid in msg.responded_entities:
            return False
        updated = False

        if isinstance(msg, ElementalReactionTriggeredMsg):
            msg = cast(ElementalReactionTriggeredMsg, msg)
            source_play_id, source_pos = msg.source
            if (
                source_play_id == self.player_id
                and not self.element_type_change
                and msg.elemental_reaction_type == ElementalReactionType.SWIRL
            ):
                self.element_type_change = True
                self.damage_element = msg.reaction_tuple[1]
            updated = True

        if isinstance(msg, RoundEndMsg):
            msg = cast(RoundEndMsg, msg)
            new_msg = DealDamageMsg(
                attack_type=AttackType.SUMMON,
                sender_id=self.player_id,
                attacker=(self.player_id, CharPos.NONE),
                targets=[
                    (
                        ~self.player_id,
                        CharPos.ACTIVE,
                        self.damage_element,
                        self.damage_value,
                    )
                ],
            )
            msg_queue.put(new_msg)
            self.usages -= 1
            if self.usages == 0:
                self.active = False
            updated = True
        if updated:
            msg.responded_entities.append(self._uuid)
        return updated


class Sucrose(CharacterCard):
    """Sucrose"""

    id: int = 1501
    name: str = "Sucrose"
    element_type: ElementType = ElementType.ANEMO
    nations: List[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.CATALYST
    skills: List[CharacterSkill] = [
        WindSpiritCreation(),
        AstableAnemohypostasisCreation6308(),
        ForbiddenCreationIsomer75TypeII(),
    ]

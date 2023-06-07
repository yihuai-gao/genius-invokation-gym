"""雷电将军"""
from queue import PriorityQueue
from typing import TYPE_CHECKING, Dict, cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    AttackType,
    CharPos,
    ElementType,
    Nation,
    SkillType,
    StatusType,
    WeaponType,
)
from gisim.classes.message import (
    ChangePowerMsg,
    DealDamageMsg,
    GenerateCharacterStatusMsg,
    RoundBeginMsg,
    RoundEndMsg,
    UseSkillMsg,
)
from gisim.classes.summon import AttackSummon
from gisim.env import INF_INT

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity


# Skill
class Origin(GenericSkill):
    """Normal Attack: Origin
    Deals 2 Physical DMG."""

    id: int = 65591
    name: str = "Origin"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class TranscendenceBalefulOmen(GenericSkill):
    """Elemental Skill: Transcendence: Baleful Omen
    Summons 1 Eye of Stormy Judgment"""

    id: int = 65592
    name: str = "Transcendence Baleful Omen"
    text: str = """
    Summons 1 Eye of Stormy Judgment
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 3}
    damage_element: ElementType = ElementType.ELECTRO
    summon_name: str = "Eye of Stormy Judgment"


class SecretArtMusouShinsetsu(GenericSkill):
    """Elemental Burst: Secret Art: Musou Shinsetsu
    Deals 3 Electro DMG. All of your other characters gain 2 Energy."""

    id: int = 65593
    name: str = "Secret Art Musou Shinsetsu"
    text: str = """Deals 3 Electro DMG. All of your other characters gain 2 Energy."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ELECTRO: 4, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 3

    def use_skill(self, msg_queue: PriorityQueue, parent: "CharacterEntity"):
        msg = msg_queue.get()
        msg = cast(UseSkillMsg, msg)
        target_player_id, target_char_pos = msg.skill_targets[0]
        new_msg = DealDamageMsg(
            attack_type=AttackType(self.type.value),
            attacker=(parent.player_id, parent.position),
            sender_id=parent.player_id,
            targets=[
                (
                    target_player_id,
                    target_char_pos,
                    self.damage_element,
                    self.damage_value,
                )
            ],
        )
        msg_queue.put(new_msg)
        new_msg = ChangePowerMsg(
            sender_id=parent.player_id,
            change_targets=[
                (
                    parent.player_id,
                    parent.position + k,
                )
                for k in [1, 2]
            ],
            change_vals=[1 for k in range(2)],
        )
        msg_queue.put(new_msg)


# Passive Skill
class ChakraDesiderata(GenericSkill):
    """Passive Skill: Chakra Desiderata
    (Passive) When the battle beings, this character gains Chakra Desiderata."""

    id: int = 65594
    name: str = "Chakra Desiderata"
    text: str = (
        """(Passive) When the battle beings, this character gains Chakra Desiderata."""
    )
    costs: Dict[ElementType, int] = {}
    type: SkillType = SkillType.PASSIVE_SKILL

    status_name: str = "Chakra Desiderata"
    status_remaining_round: int = INF_INT
    status_remaining_usage: int = INF_INT
    status_buff_type: StatusType = StatusType.ATTACK_BUFF

    def use_skill(self, msg_queue: PriorityQueue, parent: "CharacterEntity"):
        top_msg = msg_queue.queue[0]
        updated = False
        # TODO : How Can Trigger at "Battle Beings"

        if isinstance(top_msg, RoundBeginMsg):
            top_msg = cast(RoundBeginMsg, top_msg)
            msg = GenerateCharacterStatusMsg(
                sender_id=parent.player_id,
                target=(parent.player_id, parent.position),
                status_name=self.status_name,
                remaining_round=self.status_remaining_round,
                remaining_usage=self.status_remaining_usage,
                status_type=self.status_buff_type,
            )
            updated = True
        return updated


# Summon
class EyeofStormyJudgment(AttackSummon):
    """Summon: Eye of Stormy Judgment
    End Phase: Deal 1 Electro DMG.
    When this Summon is on the field: Your characters' Elemental Bursts deal +1 DMG.
    Usage(s): 3."""

    name: str = "Eye of Stormy Judgment"
    usages: int = 3
    damage_element: ElementType = ElementType.ELECTRO
    damage_value: int = 1

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False
        if isinstance(top_msg, RoundEndMsg):
            top_msg = cast(RoundEndMsg, top_msg)
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

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            attacker_id, attacker_pos = top_msg.attacker
            if (
                attacker_id == self.player_id
                and top_msg.attack_type == AttackType.ELEMENTAL_BURST
            ):
                for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                    top_msg.targets
                ):
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val + 1,
                    )
            updated = True

        if updated:
            top_msg.responded_entities.append(self._uuid)
        return updated


class RaidenShogun(CharacterCard):
    """Raiden Shogun"""

    id: int = 6559
    name: str = "Raiden Shogun"
    element_type: ElementType = ElementType.ELECTRO
    nations: list[Nation] = [Nation.Inazuma]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.POLEARM
    skills: list[CharacterSkill] = [
        Origin(),
        TranscendenceBalefulOmen(),
        SecretArtMusouShinsetsu(),
        ChakraDesiderata(),
    ]

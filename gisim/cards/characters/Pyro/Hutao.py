"""胡桃"""
from queue import PriorityQueue
from typing import TYPE_CHECKING, Dict, List, cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import AttackType, ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import DealDamageMsg, HealHpMsg, RoundEndMsg, UseSkillMsg
from gisim.classes.status import CharacterStatusEntity
from gisim.env import INF_INT

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity


class SecretSpearofWangsheng(GenericSkill):
    """Normal Attack: Secret Spear of Wangsheng
    Deals 2 Physical DMG.
    """

    id: int = 65581
    name: str = "Secret Spear of Wangsheng"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.PYRO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class GuidetoAfterlife(GenericSkill):
    """Elemental Skill: Guide to Afterlife
    This character gains [Paramita Papilio].
    """

    id: int = 65582
    name: str = "Guide to Afterlife"
    text: str = """
    This character gains [Paramita Papilio].
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.PYRO: 2}
    status_name: str = "Paramita Papilio"
    status_id: int = 113071

    status_remaining_round: int = 2
    status_remaining_usage: int = INF_INT


class SpiritSoother(GenericSkill):
    """Elemental Burst: Spirit Soother
    Deals 4 Pyro DMG, heals herself for 2 HP.
    If this character's HP is no more than 6,
    DMG dealt and Healing are increased by 1.
    """

    id: int = 65583
    name: str = "Spirit Soother"
    text: str = """
    Deals 4 Pyro DMG, heals herself for 2 HP. If this character's HP is no more than 6, DMG dealt and Healing are increased by 1.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.PYRO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.PYRO
    damage_value: int = 4
    heal_value: int = 2

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
                    self.damage_value + 1
                    if parent.health_point <= 6
                    else self.damage_value,
                )
            ],
        )
        msg_queue.put(new_msg)
        new_msg = HealHpMsg(
            sender_id=parent.player_id,
            targets=[
                (
                    parent.player_id,
                    parent.position,
                    self.heal_value + 1
                    if parent.health_point <= 6
                    else self.heal_value,
                )
            ],
        )
        msg_queue.put(new_msg)


class Hutao(CharacterCard):
    """胡桃"""

    id: int = 6558
    name: str = "Hutao"
    element_type: ElementType = ElementType.PYRO
    nations: List[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.POLEARM
    skills: List[CharacterSkill] = [
        SecretSpearofWangsheng(),
        GuidetoAfterlife(),
        SpiritSoother(),
    ]


class ParamitaPapilioStatus(CharacterStatusEntity):
    """The character to which this is attached has their Physical DMG dealt converted to Pyro DMG,
    and they will deal +1 Pyro DMG.Some times can Apply [Blood Blossom].
    Duration (Rounds): 2
    """

    id: int = 113071
    name: str = "Paramita Papilio"
    element: ElementType = ElementType.PYRO
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
                for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                    top_msg.targets
                ):
                    print(
                        f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} + Add: 1\n        {self.player_id.name}-{self.position}\n"
                    )
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        self.element
                        if element_type is ElementType.NONE
                        else element_type,
                        dmg_val + 1,
                    )
                    updated = True

        if isinstance(top_msg, RoundEndMsg):
            self.remaining_round -= 1

            if self.remaining_round == 0:
                self.remaining_usage = 0
                self.active = False

        # TODO Charged Attack: Apply Blood Blossom to target character.

        if updated:
            top_msg.responded_entities.append(self._uuid)

        return updated


class BloodBlossomStatus(CharacterStatusEntity):
    """End Phase: Deal 1 Pyro DMG to the character to which this is attached.
    Usage(s): 1
    """

    id: int = 1009
    name: str = "Paramita Papilio"
    element: ElementType = ElementType.PYRO
    description: str = """End Phase: Deal 1 Pyro DMG to the character to which this is attached. Usage(s): 1"""
    value: int = 0
    active: bool = True
    remaining_round: int = 1
    remaining_usage: int = 1

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False
        if isinstance(top_msg, RoundEndMsg):
            new_msg = DealDamageMsg(
                sender_id=self.player_id,
                attack_type=AttackType.COMBAT_STATUS,
                attacker=(self.player_id, self.position),
                targets=[(self.player_id, self.position, self.element, 1)],
            )
            msg_queue.put(new_msg)
            self.remaining_usage -= 1
            self.remaining_round -= 1
            self.active = False
            updated = True

        if updated:
            top_msg.responded_entities.append(self._uuid)

        return updated

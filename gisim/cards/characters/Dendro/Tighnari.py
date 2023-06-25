from queue import PriorityQueue
from typing import cast

from classes.message import DealDamageMsg, RoundEndMsg
from classes.status import CharacterStatusEntity
from env import INF_INT

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


class VijanaSuffusionStatus(CharacterStatusEntity):
    name: str = "VijanaSuffusion"
    element: ElementType = ElementType.DENDRO
    description: str = "Convert physical damage into elemental damage"
    value: int = 0
    active: bool = True
    remaining_usage: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attacker == (self.player_id, self.position):
                for idx, target in enumerate(top_msg.targets):
                    if target[2] == ElementType.NONE:
                        print(
                            f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {target[2]} -> {target[3]} + Add: 0\n        {self.player_id.name}-{self.position}\n"
                        )
                        top_msg.targets[idx] = (
                            target[0],
                            target[1],
                            self.element,
                            target[3],
                        )
                        updated = True

        if isinstance(top_msg, RoundEndMsg):
            top_msg = cast(RoundEndMsg, top_msg)
            assert (
                self.remaining_round >= 1
            ), "Remaining round should not be lower than 1!"
            self.remaining_round -= 1
            if self.remaining_round == 0:
                self.active = False
        if updated:
            top_msg.responded_entities.append(self._uuid)
        return updated

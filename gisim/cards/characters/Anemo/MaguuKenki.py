"""MaguuKenki: 剑鬼魔偶"""

from queue import PriorityQueue
from typing import TYPE_CHECKING, Dict, List, cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    AttackType,
    CharPos,
    ElementType,
    Nation,
    SkillType,
    WeaponType,
)
from gisim.classes.message import DealDamageMsg, TriggerSummonEffectMsg, UseSkillMsg
from gisim.classes.summon import AttackSummon

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity


class Ichimonji(GenericSkill):
    """Normal Attack: Ichimonji
    Deals 2 Physical DMG."""

    id: int = 25011
    name: str = "Ichimonji"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class BlusteringBlade(GenericSkill):
    """Elemental Skill: Blustering Blade
    Summons 1 Shadowsword: Lone Gale."""

    id: int = 25012
    name: str = "Blustering Blade"
    text: str = """
    Summons 1 Shadowsword: Lone Gale.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 3}
    summon_name: str = "Shadowsword Lone Gale"
    summon_id: int = 125011


class ShadowswordLoneGale(AttackSummon):
    """Summon: Shadowsword: Lone Gale
    End Phase: Deal 1 Anemo DMG.
    Usage(s): 2"""

    id: int = 125011
    name: str = "Shadowsword Lone Gale"
    usages: int = 2
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 1


class FrostyAssault(GenericSkill):
    """Elemental Skill: Frosty Assault
    Summons 1 Shadowsword: Galloping Frost."""

    id: int = 25013
    name: str = "Frosty Assault"
    text: str = """
    Summons 1 Shadowsword: Galloping Frost.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: Dict[ElementType, int] = {ElementType.CRYO: 3}
    summon_name: str = "Shadowsword Galloping Frost"


class ShadowswordGallopingFrost(AttackSummon):
    """Shadowsword: Galloping Frost
    End Phase: Deal 1 Cryo DMG.
    Usage(s): 2"""

    id: int = 125012
    name: str = "Shadowsword Galloping Frost"
    usages: int = 2
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 1


class PseudoTenguSweeper(GenericSkill):
    """Elemental Burst: Pseudo Tengu Sweeper
    Deals 4 Anemo DMG, triggers the effect(s) of all your Shadowsword Summon(s).
    (Does not consume their Usages)"""

    id: int = 25014
    name: str = "Pseudo Tengu Sweeper"
    text: str = """Deals 4 Anemo DMG, triggers the effect(s) of all your Shadowsword Summon(s). (Does not consume their Usages)"""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: Dict[ElementType, int] = {ElementType.ANEMO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 4

    def use_skill(self, msg_queue: PriorityQueue, parent: "CharacterEntity"):
        top_msg = msg_queue.queue[0]
        msg = cast(UseSkillMsg, top_msg)

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
        new_msg = TriggerSummonEffectMsg(
            sender_id=parent.player_id,
            summon_list=["Shadowsword Galloping Frost", "Shadowsword Lone Gale"],
        )
        msg_queue.put(new_msg)


class MaguuKenki(CharacterCard):
    """MaguuKenki"""

    id: int = 2501
    name: str = "Maguu Kenki"
    element_type: ElementType = ElementType.ANEMO
    nations: List[Nation] = [Nation.Monster]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: List[CharacterSkill] = [
        Ichimonji(),
        BlusteringBlade(),
        FrostyAssault(),
        PseudoTenguSweeper(),
    ]

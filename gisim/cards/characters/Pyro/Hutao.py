"""胡桃"""
from queue import PriorityQueue
from typing import TYPE_CHECKING, Dict, List, cast

from gisim.cards.characters.base import (CharacterCard, CharacterSkill,
                                         GenericSkill)
from gisim.classes.enums import (ElementType, Nation, SkillType, StatusType,
                                 WeaponType,AttackType)
from gisim.classes.message import DealDamageMsg, HealHpMsg, UseSkillMsg
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
    costs: dict[ElementType, int] = {ElementType.PYRO: 1, ElementType.ANY: 2}
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
    costs: dict[ElementType, int] = {ElementType.PYRO: 2}
    status_name: str = "Paramita Papilio"
    status_remaining_round: int = 2
    status_remaining_usage: int = INF_INT
    status_buff_type: StatusType = StatusType.ATTACK_BUFF


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
    costs: dict[ElementType, int] = {ElementType.PYRO: 3, ElementType.POWER: 3}
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
                    self.damage_value + 1 if parent.health_point <= 6 else self.damage_value
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
                    self.heal_value + 1 if parent.health_point <= 6 else self.heal_value
                )
            ],
        )
        msg_queue.put(new_msg)


class Hutao(CharacterCard):
    """胡桃"""
    id: int = 6558
    name: str = "Hutao"
    element_type: ElementType = ElementType.PYRO
    nations: list[Nation] = [Nation.Liyue]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.POLEARM
    skills: list[CharacterSkill] = [
        SecretSpearofWangsheng(),
        GuidetoAfterlife(),
        SpiritSoother(),
    ]

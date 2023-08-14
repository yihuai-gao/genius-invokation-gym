"""迪奥娜"""
from queue import PriorityQueue
from typing import cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    AttackType,
    CharPos,
    ElementType,
    EntityType,
    EquipmentType,
    Nation,
    PlayerID,
    SkillType,
    WeaponType,
)
from gisim.classes.message import DealDamageMsg, HealHpMsg, RoundEndMsg
from gisim.classes.status import CombatStatusEntity
from gisim.classes.summon import AttackSummon


class KatzleinStyle(GenericSkill):
    """
    猎人射术
    ~~~~~~~~
    造成2点`物理伤害`。
    """

    id: int = 11021
    name: str = "Katzlein Style"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.CRYO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class IcyPaws(GenericSkill):
    """
    猫爪冻冻
    ~~~~~~~~
    造成2点`冰元素伤害`，生成`猫爪护盾`。
    """

    id: int = 11022
    name: str = "Icy Paws"
    text: str = """
    Deals 2 Cryo DMG, creates 1 Cat-Claw Shield.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2
    combat_status_name: str = "Shield"
    combat_status_remaining_usage: int = 1


class SignatureMix(GenericSkill):
    """
    最烈特调
    ~~~~~~~~
    造成1点`冰元素伤害`，治疗此角色2点，召唤`酒雾领域`。
    """

    id: int = 11023
    name: str = "Signature Mix"
    text: str = """
    Deals 1 Cryo DMG, heals this character for 2 HP, summons 1 Drunken Mist.
    """
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.CRYO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 1
    summon_name: str = "Drunken Mist"
    summon_id: int = 111023


class DrunkenMist(AttackSummon):
    """Drunken Mist
    End Phase: Deal 1 Cryo DMG, heal your active character for 2 HP.
    Usage(s): 2"""

    id: int = 111023
    name: str = "Drunken Mist"
    usages: int = 2
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 1

    def msg_handler(self, msg_queue):
        msg = msg_queue.queue[0]
        if self._uuid in msg.responded_entities:
            return False
        updated = False

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
            new_msg = HealHpMsg(
                sender_id=self.player_id, targets=[(self.player_id, CharPos.ACTIVE, 2)]
            )
            msg_queue.put(new_msg)
            self.usages -= 1
            if self.usages == 0:
                self.active = False
            updated = True

        if updated:
            msg.responded_entities.append(self._uuid)
        return updated


class Diona(CharacterCard):
    """迪奥娜"""

    id: int = 1102
    name: str = "Diona"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.BOW
    skills: list[CharacterSkill] = [
        KatzleinStyle(),
        IcyPaws(),
        SignatureMix(),
    ]

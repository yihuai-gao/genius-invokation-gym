"""Maguu Kenki"""
from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import (
    ElementType,
    Nation,
    SkillType,
    WeaponType,
    AttackType,
    CharPos
)
from typing import cast
from gisim.classes.summon import AttackSummon
from gisim.classes.message import RoundEndMsg, DealDamageMsg, AfterUsingSkillMsg


class Ichimonji(GenericSkill):
    """Normal Attack: Ichimonji
    Deals 2 Physical DMG."""
    id: int = 25011
    name: str = "Ichimonji"
    text: str = """
    Deals 2 Physical DMG.
    """
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
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
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3}
    summon_name: str = "Shadowsword Lone Gale"


class ShadowswordLoneGale(AttackSummon):
    """Summon: Shadowsword: Lone Gale
    End Phase: Deal 1 Anemo DMG.
    Usage(s): 2"""
    name: str = "Shadowsword Lone Gale"
    usages: int = 2
    damage_element: ElementType = ElementType.ANEMO
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
            self.usages -= 1
            if self.usages == 0:
                self.active = False
            msg.responded_entities.append(self._uuid)
            updated = True
        if isinstance(msg, AfterUsingSkillMsg):
            # If Maguu Kenki use Element Burst
            msg = cast(AfterUsingSkillMsg, msg)
            if msg.skill_name == "Pseudo Tengu Sweeper":
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
            updated = True

        return updated


class FrostyAssault(GenericSkill):
    """Elemental Skill: Frosty Assault
    Summons 1 Shadowsword: Galloping Frost."""
    id: int = 25013
    name: str = "Frosty Assault"
    text: str = """
    Summons 1 Shadowsword: Galloping Frost.
    """
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    summon_name: str = "Shadowsword Galloping Frost"


class ShadowswordGallopingFrost(AttackSummon):
    """Shadowsword: Galloping Frost
    End Phase: Deal 1 Cryo DMG.
    Usage(s): 2"""
    name: str = "Shadowsword Galloping Frost"
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
            self.usages -= 1
            if self.usages == 0:
                self.active = False
            msg.responded_entities.append(self._uuid)
            updated = True
            
        if isinstance(msg, AfterUsingSkillMsg):
            # If Maguu Kenki use Element Burst
            msg = cast(AfterUsingSkillMsg, msg)
            if msg.skill_name == "Pseudo Tengu Sweeper":
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
            updated = True

        return updated


class PseudoTenguSweeper(GenericSkill):
    """Elemental Burst: Pseudo Tengu Sweeper
    Deals 4 Anemo DMG, triggers the effect(s) of all your Shadowsword Summon(s). 
    (Does not consume their Usages)"""
    id: int = 25014
    name: str = "Pseudo Tengu Sweeper"
    text: str = """Deals 4 Anemo DMG, triggers the effect(s) of all your Shadowsword Summon(s). (Does not consume their Usages)"""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {
        ElementType.ANEMO: 3, ElementType.POWER: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 4


class MaguuKenki(CharacterCard):
    """魔偶剑鬼"""
    id: int = 2501
    name: str = "Maguu Kenki"
    element_type: ElementType = ElementType.ANEMO
    nations: list[Nation] = [Nation.Monster]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.OTHER_WEAPONS
    skills: list[CharacterSkill] = [
        Ichimonji(),
        BlusteringBlade(),
        FrostyAssault(),
        PseudoTenguSweeper(),
    ]

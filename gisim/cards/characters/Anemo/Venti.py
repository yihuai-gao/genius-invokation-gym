"""Venti"""
from queue import PriorityQueue
from typing import cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import PayChangeCharacterCostMsg
from gisim.classes.status import CombatStatusEntity
from gisim.classes.summon import AttackSummon
from gisim.env import INF_INT


class DivineMarksmanship(GenericSkill):
    """Normal Attack: Divine Marksmanship
    Deals 2 Physical DMG."""

    id: int = 65611
    name: str = "Divine Marksmanship"
    text: str = """Deals 2 Physical DMG."""
    type: SkillType = SkillType.NORMAL_ATTACK
    costs: dict[ElementType, int] = {ElementType.ANEMO: 1, ElementType.ANY: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 2


class SkywardSonnet(GenericSkill):
    """Elemental Skill: Skyward Sonnet
    Deals 2 Anemo DMG, creates 1 Stormzone."""

    id: int = 65612
    name: str = "Skyward Sonnet"
    text: str = """Deals 2 Anemo DMG, creates 1 Stormzone."""
    type: SkillType = SkillType.ELEMENTAL_SKILL
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 2


class Stormzone(CombatStatusEntity):
    """Combat Status: Stormzone
    When you perform "Switch Character": Spend 1 less Elemental Die.
    Usage(s): 2
    """

    name: str = "Stormzone"
    description: str = """When you perform "Switch Character": Spend 1 less Elemental Die.Usage(s): 2"""
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 2

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        if isinstance(top_msg, PayChangeCharacterCostMsg):
            top_msg = cast(PayChangeCharacterCostMsg, top_msg)
            if top_msg.sender_id == self.player_id:
                top_msg.paid_dice_idx -= 1
                self.remaining_usage -= 1
        # TODO: Spend 1 less Elemental Die


class WindsGrandOde(GenericSkill):
    """Elemental Burst: Wind's Grand Ode
    Deals 2 Anemo DMG, summons 1 Stormeye."""

    id: int = 65613
    name: str = "Winds Grand Ode"
    text: str = """Deals 2 Anemo DMG, summons 1 Stormeye."""
    type: SkillType = SkillType.ELEMENTAL_BURST
    costs: dict[ElementType, int] = {ElementType.ANEMO: 3, ElementType.POWER: 2}
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 2


class Stormeye(AttackSummon):
    """Summon: Stormeye
    End Phase: Deal 2 Anemo DMG. Your opponent switches to: Character Closest to Your Current Active Character.
    After your character or Summon triggers a Swirl reaction: Convert the Elemental Type of this card and change its DMG dealt to the element Swirled. (Can only be converted once before leaving the field)
    Character Closest to Your Current Active Character
    The opposing "character closest to your current active character" is the opposing character whose position is closest to that of your active character.
    If multiple such characters exist, the one with the foremost position will be viewed as being "closest."
    Usage(s): 2
    """

    name: str = "Stormeye"
    usages: int = 2
    damage_element: ElementType = ElementType.ANEMO
    damage_value: int = 2
    # TODO: What is the character closest to the current active character


class Venti(CharacterCard):
    """Venti"""

    id: int = 5651
    name: str = "Sucrose"
    element_type: ElementType = ElementType.ANEMO
    nations: list[Nation] = [Nation.Mondstadt]
    health_point: int = 10
    power: int = 0
    max_power: int = 2
    weapon_type: WeaponType = WeaponType.BOW
    skills: list[CharacterSkill] = [
        DivineMarksmanship(),
        SkywardSonnet(),
        WindsGrandOde(),
    ]

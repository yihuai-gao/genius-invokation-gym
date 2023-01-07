"""神里绫华"""

from queue import PriorityQueue
from typing import TYPE_CHECKING, cast
from xml.dom.minidom import Element

from gisim.cards.characters.base import (
    CharacterCard,
    CharacterSkill,
    register_character_skill_factory,
)
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import DealDamageMsg, Message, PaySkillCostMsg, UseSkillMsg

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity


class KamisatoArtKabuki(CharacterSkill):
    id: int = 11051
    name: str = "Kamisato Art: Kabuki"
    text: str = """
    Kamisato Art: Kabuki / 神里流·倾
    """
    costs: dict[ElementType, int] = {ElementType.CRYO: 1, ElementType.ANY: 2}
    types: list[SkillType] = [SkillType.NORMAL_ATTACK]

    def use_skill(self, msg_queue: PriorityQueue[Message], parent: "CharacterEntity"):
        msg = msg_queue.get()
        msg = cast(UseSkillMsg, msg)
        target_player_id, target_char_pos = msg.skill_targets[0]
        new_msg = DealDamageMsg(
            sender_id=parent.player_id,
            targets=[(target_player_id, target_char_pos, ElementType.NONE, 2)],
        )
        msg_queue.put(new_msg)


class KamisatoArtHyouka(CharacterSkill):
    id: int = 11052
    name: str = "Kamisato Art: Hyouka"
    text: str = """
    Kamisato Art: Hyouka / 神里流·冰华
    """
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    types: list[SkillType] = [SkillType.ELEMENTAL_SKILL]

    def use_skill(self, msg_queue: PriorityQueue[Message], parent: "CharacterEntity"):
        msg = msg_queue.get()
        msg = cast(UseSkillMsg, msg)
        target_player_id, target_char_pos = msg.skill_targets[0]
        new_msg = DealDamageMsg(
            sender_id=parent.player_id,
            targets=[(target_player_id, target_char_pos, ElementType.CRYO, 3)],
        )
        msg_queue.put(new_msg)


class KamisatoArtSoumetsu(CharacterSkill):
    id: int = 11053
    name: str = "Kamisato Art: Soumetsu"
    text: str = """
    Kamisato Art: Soumetsu / 神里流·霜灭
    """
    costs: dict[ElementType, int] = {ElementType.CRYO: 3, ElementType.POWER: 3}
    types: list[SkillType] = [SkillType.ELEMENTAL_BURST]

    def use_skill(self, msg_queue: PriorityQueue[Message], parent: "CharacterEntity"):
        msg = msg_queue.get()
        msg = cast(UseSkillMsg, msg)
        target_player_id, target_char_pos = msg.skill_targets[0]
        new_msg = DealDamageMsg(
            sender_id=parent.player_id,
            targets=[(target_player_id, target_char_pos, ElementType.CRYO, 4)],
        )
        # TODO: Generate a summon
        msg_queue.put(new_msg)


class KamisatoArtSenho(CharacterSkill):

    id: int = 11054
    name: str = "Kamisato Art: Senho"
    text: str = """
    Kamisato Art: Senho / 神里流·霰步
    (Passive) When switched to be the active character, this character gains Cryo Elemental Infusion.
    【被动】此角色被切换为「出战角色」时，附属冰元素附魔。
    """
    costs: dict[ElementType, int] = {}
    types: list[SkillType] = [SkillType.PASSIVE_SKILL]

    def use_skill(self, msg_queue: PriorityQueue[Message], parent: "CharacterEntity"):
        msg = msg_queue.get()
        msg = cast(UseSkillMsg, msg)
        target_player_id, target_char_pos = msg.skill_targets[0]
        new_msg = DealDamageMsg(
            sender_id=parent.player_id,
            targets=[(target_player_id, target_char_pos, ElementType.NONE, 2)],
        )
        msg_queue.put(new_msg)


class KamisatoAyaka(CharacterCard):
    id: int = 1105
    name: str = "Kamisato Ayaka"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Inazuma]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.SWORD
    skills: list[CharacterSkill] = [
        KamisatoArtKabuki(),
        KamisatoArtHyouka(),
        KamisatoArtSoumetsu(),
        KamisatoArtSenho(),
    ]

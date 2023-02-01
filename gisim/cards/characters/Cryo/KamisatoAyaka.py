"""神里绫华"""

from queue import PriorityQueue
from typing import TYPE_CHECKING, cast

from gisim.cards.characters.base import CharacterCard, CharacterSkill, GenericSkill
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import (
    ChangeCharacterMsg,
    GenerateCharacterStatusMsg,
    Message,
)
from gisim.classes.summon import AttackSummon, Summon
from gisim.env import INF_INT

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity


class KamisatoArtKabuki(GenericSkill):
    id: int = 11051
    name: str = "Kamisato Art: Kabuki"
    text: str = """
    Deals 2 Physical DMG.
    """
    costs: dict[ElementType, int] = {ElementType.CRYO: 1, ElementType.ANY: 2}
    type: SkillType = SkillType.NORMAL_ATTACK
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 2


class KamisatoArtHyouka(GenericSkill):
    id: int = 11052
    name: str = "Kamisato Art: Hyouka"
    text: str = """
    Deals 3 Cryo DMG
    """
    costs: dict[ElementType, int] = {ElementType.CRYO: 3}
    type: SkillType = SkillType.ELEMENTAL_SKILL
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 3


class KamisatoArtSoumetsu(GenericSkill):
    id: int = 11053
    name: str = "Kamisato Art: Soumetsu"
    text: str = """
    Deals 4 Cryo DMG, summons 1 Frostflake Seki no To.
    """
    costs: dict[ElementType, int] = {ElementType.CRYO: 3, ElementType.POWER: 3}
    type: SkillType = SkillType.ELEMENTAL_BURST
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 4
    summon_name: str = "Frostflake Seki no To"


class KamisatoArtSenho(CharacterSkill):

    id: int = 11054
    name: str = "Kamisato Art: Senho"
    text: str = """
    (Passive) When switched to be the active character, this character gains Cryo Elemental Infusion.
    """
    costs: dict[ElementType, int] = {}
    type: SkillType = SkillType.PASSIVE_SKILL

    def use_skill(self, msg_queue: PriorityQueue[Message], parent: "CharacterEntity"):
        top_msg = msg_queue.queue[0]
        updated = False
        if isinstance(top_msg, ChangeCharacterMsg):
            top_msg = cast(ChangeCharacterMsg, top_msg)
            if top_msg.target == (parent.player_id, parent.position):
                new_msg = GenerateCharacterStatusMsg(
                    sender_id=parent.player_id,
                    status_name="Cryo Infusion",
                    target=(parent.player_id, parent.position),
                    remaining_round=1,
                    remaining_usage=INF_INT,
                )
                msg_queue.put(new_msg)
                updated = True

        return updated


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


class FrostflakeSekinoTo(AttackSummon):
    name: str = "Frostflake Seki no To"
    usages: int = 2
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2

"""神里绫华"""

from queue import PriorityQueue

from gisim.cards.characters.base import CharacterSkill, register_character_skill_factory
from gisim.classes.enums import CharacterPosition, MsgPriority
from gisim.classes.message import Message, UseSkillMsg


@register_character_skill_factory(11054)
class KamisatoAyakaSenho(CharacterSkill):
    """
    Kamisato Art: Senho / 神里流·霰步
    (Passive) When switched to be the active character, this character gains <color=#FFFFFFFF>Cryo Elemental Infusion</color>.
    【被动】此角色被切换为「出战角色」时，附属<color=#FFFFFFFF>冰元素附魔</color>。
    """

    def on_skill(self) -> list:
        # This is just a placeholder, you need to replace it with your own implementation
        return self._build_message(
            "Inufsion", ("cryo",), conditions={"on_switch": True}
        )

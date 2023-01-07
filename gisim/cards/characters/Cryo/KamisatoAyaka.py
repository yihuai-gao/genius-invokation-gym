"""神里绫华"""

from queue import PriorityQueue
from typing import TYPE_CHECKING, cast
from xml.dom.minidom import Element

from gisim.cards.characters.base import CharacterCard, CharacterSkill, register_character_skill_factory
from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import DealDamageMsg, Message, PaySkillCostMsg, UseSkillMsg

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity

class KamisatoArtSenho(CharacterSkill):
    
    id:int = 11054
    text:str = """
    Kamisato Art: Senho / 神里流·霰步
    (Passive) When switched to be the active character, this character gains Cryo Elemental Infusion.
    【被动】此角色被切换为「出战角色」时，附属冰元素附魔。
    """
    name:str = "Kamisato Art: Senho"
    costs: dict[ElementType, int] = {ElementType.CRYO:1, ElementType.ANY:2}
    types: list[SkillType] = [SkillType.NORMAL_ATTACK]
    
    def use_skill(self, msg_queue: PriorityQueue[Message], parent:"CharacterEntity"):
        msg = msg_queue.get()
        msg = cast(UseSkillMsg, msg)
        target_player_id, target_char_pos = msg.skill_targets[0]
        new_msg = DealDamageMsg(
            sender_id=parent.player_id, 
            targets=[(target_player_id, target_char_pos, ElementType.NONE, 2)],
            )
        msg_queue.put(new_msg)
                
                


            
            
    # def on_skill(self) -> list:
    # This is just a placeholder, you need to replace it with your own implementation
    # return self._build_message(
    #     "Inufsion", ("cryo",), conditions={"on_switch": True}
    # )

class KamisatoAyaka(CharacterCard):
    id:int = 1105
    name:str = "Kamisato Ayaka"
    element_type: ElementType = ElementType.CRYO
    nations: list[Nation] = [Nation.Inazuma]
    health_point: int = 10
    power: int = 0
    max_power: int = 3
    weapon_type: WeaponType = WeaponType.SWORD
    skills: list[CharacterSkill] = [KamisatoArtSenho()]
    

# @register_character_skill_factory(11054)



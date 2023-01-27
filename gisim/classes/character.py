"""Base class of each character: abstract class
A character in the game should be an instant of the specific character class defined in each file"""
from abc import ABC, abstractmethod
from collections import OrderedDict
from queue import PriorityQueue
from typing import Optional, cast

from pydantic import PrivateAttr

from gisim.cards.characters import get_character_card
from gisim.cards.characters.base import CharacterCard, CharacterSkill

from .entity import Entity
from .enums import *
from .message import (
    AfterUsingSkillMsg,
    ChangeCharacterMsg,
    CharacterDiedMsg,
    DealDamageMsg,
    Message,
    PaySkillCostMsg,
    UseSkillMsg,
)

# from gisim.cards.characters.base import (
#     CHARACTER_CARDS,
#     CHARACTER_NAME2ID,
#     CHARACTER_SKILLS,
# )


class CharacterEntity(Entity):
    name: str
    player_id: PlayerID
    position: CharPos
    active: bool = False
    """ Whether this character in set forward. There should be only one character in the active state for each player"""
    alive: bool = True
    elemental_attachment = ElementType.NONE
    """角色元素附着"""

    character_card: CharacterCard
    id: int
    element_type: ElementType
    nationalities: list[Nation]
    weapon_type: WeaponType
    skills: list[CharacterSkill]
    skill_num: int
    skill_names: list[str]
    health_point: int
    power: int
    max_power: int

    def __init__(self, name: str, player_id: PlayerID, position: CharPos):
        card = get_character_card(name)
        skills = card.skills.copy()
        attrs = {
            "name": name,
            "player_id": player_id,
            "position": position,
            "active": False,
            "alive": True,
            "character_card": card,
            "id": card.id,
            "element_type": card.element_type,
            "nationalities": card.nations,
            "weapon_type": card.weapon_type,
            "skills": skills,
            "skill_num": len(skills),
            "skill_names": [skill.name for skill in skills],
            "health_point": card.health_point,
            "power": card.power,
            "max_power": card.max_power,
        }
        super().__init__(**attrs)

    def encode(self):
        properties = [
            "name",
            "active",
            "alive",
            "elemental_attachment",
            "health_point",
            "power",
            "max_power",
        ]
        return {key: getattr(self, key) for key in properties}

    def get_skill(
        self,
        id: Optional[int] = None,
        skill_name: Optional[str] = None,
        skill_type: Optional[SkillType] = None,
    ):
        """Get the character's skill through either id (0, 1, 2, ...), name (str), or skill_type
        Returns:
            skill (Skill): a Skill object with raw cost and effects (has not been affected by any discounts/enhancement)
        """
        if id is not None:
            assert (
                0 <= id <= self.skill_num - 1
            ), f"id should be from 0 to {self.skill_num-1}"
            return self.skills[id]
        elif skill_name is not None:
            assert (
                skill_name in self.skill_names
            ), f"Skill {skill_name} does not exist in {self.name}'s skill set."
            return self.skills[self.skill_names.index(skill_name)]
        else:
            assert skill_type is not None, "Should provide either skill id or its name."
            skill_types = [skill.type for skill in self.skills]
            assert skill_type in skill_types, f"Skill type {skill_type} does not exist."
            assert (
                skill_types.count(skill_type) == 1
            ), f"Skill type {skill_type} is not unique."
            return self.skills[skill_types.index(skill_type)]

    def passive_skill_handler(self, msg_queue: PriorityQueue[Message]):
        updated = False
        for skill in self.skills:
            if skill.type == SkillType.PASSIVE_SKILL:
                updated = skill.use_skill(msg_queue=msg_queue, parent=self)
        return updated

    def msg_handler(self, msg_queue: PriorityQueue[Message]):
        """Will respond to `UseSkillMsg` etc."""
        msg = msg_queue.queue[0]
        if self._uuid in msg.responded_entities:
            return False
        updated = self.passive_skill_handler(msg_queue)
        if isinstance(msg, PaySkillCostMsg):
            msg = cast(PaySkillCostMsg, msg)
            if msg.user_pos == self.position:
                msg = msg_queue.get()
                msg = cast(PaySkillCostMsg, msg)
                skill = self.get_skill(skill_name=msg.skill_name)
                msg.required_cost = skill.costs
                msg_queue.put(msg)
                if ElementType.POWER in skill.costs.keys():
                    self.power = self.power - skill.costs[ElementType.POWER]
                updated = True
        elif isinstance(msg, UseSkillMsg):
            msg = cast(UseSkillMsg, msg)
            if msg.user_pos == self.position:
                skill_name = msg.skill_name
                skill = self.get_skill(skill_name=skill_name)
                skill.use_skill(msg_queue=msg_queue, parent=self)
                updated = True
        elif isinstance(msg, AfterUsingSkillMsg):
            msg = cast(AfterUsingSkillMsg, msg)
            if msg.sender_id == self.player_id and msg.user_pos == self.position:
                skill_name = msg.skill_name
                skill = self.get_skill(skill_name=skill_name)
                if skill.accumulate_power and skill.type != SkillType.ELEMENTAL_BURST:
                    self.power = min(
                        self.power + skill.accumulate_power, self.max_power
                    )
                updated = True
        elif isinstance(msg, ChangeCharacterMsg):
            msg = cast(ChangeCharacterMsg, msg)
            if self.player_id == msg.target[0]:
                if self.position == msg.target[1]:
                    self.active = True
                    updated = True
                elif self.position != msg.target[1] and self.active:
                    self.active = False
                    updated = True

        elif isinstance(msg, DealDamageMsg):
            msg = cast(DealDamageMsg, msg)
            for target_id, target_pos, element_type, dmg_val in msg.targets:
                is_target = (
                    self.position == target_pos
                    or self.active
                    and target_pos == CharPos.ACTIVE
                )
                if self.player_id == target_id and is_target:
                    if self.elemental_attachment == ElementType.NONE:
                        self.elemental_attachment = element_type
                    else:
                        # TODO: add elemental reaction effects
                        pass
                    self.health_point -= min(self.health_point, dmg_val)
                    if self.health_point == 0:
                        self.alive = False
                        # self.active = False
                        dead_msg = CharacterDiedMsg(
                            sender_id=self.player_id,
                            target=(self.player_id, self.position),
                        )
                        msg_queue.put(dead_msg)
                    updated = True
        if updated:
            msg.responded_entities.append(self._uuid)
        return updated


class CharacterEntityInfo:
    def __init__(self, character_entity_info_dict: OrderedDict):
        self.name: str = character_entity_info_dict["name"]
        self.active: bool = character_entity_info_dict["active"]
        self.alive: bool = character_entity_info_dict["alive"]
        self.elemental_attachment: ElementType = character_entity_info_dict[
            "elemental_attachment"
        ]
        self.health_point: int = character_entity_info_dict["health_point"]
        self.power: int = character_entity_info_dict["power"]
        self.max_power: int = character_entity_info_dict["max_power"]

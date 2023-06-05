"""
Basic character card classes
"""
from queue import PriorityQueue
from typing import TYPE_CHECKING, Dict, List, Optional, cast

from pydantic import BaseModel, Field, validator

from gisim.classes.enums import AttackType, ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import (
    DealDamageMsg,
    GenerateCharacterStatusMsg,
    GenerateCombatStatusMsg,
    GenerateSummonMsg,
    HealHpMsg,
    Message,
    StatusType,
    UseSkillMsg,
)
from gisim.classes.reaction import element_reaction
from gisim.env import get_display_text

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity


class CharacterSkill(BaseModel):
    id: int
    name: str
    text: str
    costs: Dict[ElementType, int]
    type: SkillType
    resource: Optional[str] = None  # 图片链接
    accumulate_power: int = 1
    """Default for elemental skills and normal attacks.
    Elemental burst will accumulate no power by default."""

    # @abstractmethod
    def use_skill(self, msg_queue: PriorityQueue, parent: "CharacterEntity"):
        """
        Called when the skill is activated, by default, it parses the skill text and
        returns a list of messages to be sent to the game
        """
        ...

    # def __str__(self):
    #     return f"<{self.id}: {get_display_text(self.name)}>"


class GenericSkill(CharacterSkill):
    damage_element: ElementType = ElementType.NONE
    damage_value: int = 0
    summon_name: str = ""

    status_name: str = ""
    """Skill description format: this character gains xxx"""
    status_remaining_round: int = 0
    status_remaining_usage: int = 0
    status_buff_type: StatusType = StatusType.ATTACK_BUFF

    combat_status_name: str = ""
    """Skill description format: creates xxx"""
    combat_status_remaining_round: int = 0
    combat_status_remaining_usage: int = 0

    piercing_damage_value: int = 0
    """Piercing damage dealt to the standby characters"""
    heal_value: int = 0
    """Heal the current character"""
    heal_all_value: int = 0
    """Heal all your alive characters"""

    self_element_attachment: ElementType = ElementType.NONE
    """Some skills will add elemental attachments to themselves, such as Xingqiu."""

    def use_skill(self, msg_queue: PriorityQueue, parent: "CharacterEntity"):
        msg = msg_queue.get()
        msg = cast(UseSkillMsg, msg)
        target_player_id, target_char_pos = msg.skill_targets[0]
        if self.damage_value > 0:
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

        if self.piercing_damage_value > 0:
            new_msg = DealDamageMsg(
                attack_type=AttackType(self.type.value),
                attacker=(parent.player_id, parent.position),
                sender_id=parent.player_id,
                targets=[
                    (
                        target_player_id,
                        target_char_pos + k,
                        ElementType.PIERCE,
                        self.piercing_damage_value,
                    )
                    for k in [1, 2]  # Deals damage to two other characters
                ],
            )
            msg_queue.put(new_msg)

        if self.summon_name:
            new_msg = GenerateSummonMsg(
                sender_id=parent.player_id, summon_name=self.summon_name
            )
            msg_queue.put(new_msg)

        if self.status_name:
            new_msg = GenerateCharacterStatusMsg(
                sender_id=parent.player_id,
                target=(parent.player_id, parent.position),
                status_name=self.status_name,
                remaining_round=self.status_remaining_round,
                remaining_usage=self.status_remaining_usage,
                status_type=self.status_buff_type,
            )
            msg_queue.put(new_msg)

        if self.combat_status_name:
            new_msg = GenerateCombatStatusMsg(
                sender_id=parent.player_id,
                target_player_id=parent.player_id,
                combat_status_name=self.combat_status_name,
                remaining_round=self.combat_status_remaining_round,
                remaining_usage=self.combat_status_remaining_usage,
            )
            msg_queue.put(new_msg)

        if self.heal_value > 0:
            new_msg = HealHpMsg(
                sender_id=parent.player_id,
                targets=[(parent.player_id, parent.position, self.heal_value)],
            )
            msg_queue.put(new_msg)

        if self.heal_all_value > 0:
            new_msg = HealHpMsg(
                sender_id=parent.player_id,
                targets=[
                    (parent.player_id, parent.position + k, self.heal_all_value)
                    for k in range(3)
                ],
            )
            msg_queue.put(new_msg)


class CharacterCard(BaseModel):
    id: int
    name: str
    element_type: ElementType
    nations: List[Nation] = Field(..., min_items=1, max_items=3)  # 所属地区/阵营
    health_point: int = 10
    skills: List[CharacterSkill]
    resource: Optional[str] = None  # 图片链接
    power: int = 0
    max_power: int
    weapon_type: WeaponType

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
            skill_ids = [skill.id for skill in self.skills]
            if id in skill_ids:
                return self.skills[skill_ids.index(id)]
            assert (
                0 <= id <= len(self.skills) - 1
            ), f"id should be from 0 to {len(self.skills) -1}"
            return self.skills[id]
        elif skill_name is not None:
            skill_names = [skill.name for skill in self.skills]
            assert (
                skill_name in skill_names
            ), f"Skill {skill_name} does not exist in {self.name}'s skill set."
            return self.skills[skill_names.index(skill_name)]
        else:
            assert skill_type is not None, "Should provide either skill id or its name."
            skill_types = [skill.type for skill in self.skills]
            assert skill_type in skill_types, f"Skill type {skill_type} does not exist."
            # assert (
            #     skill_types.count(skill_type) == 1
            # ), f"Skill type {skill_type} is not unique."
            """某些角色有2个战技"""
            return self.skills[skill_types.index(skill_type)]

    @validator("element_type")
    def element_type_validator(cls, v):
        assert v not in [
            ElementType.POWER,
            ElementType.SAME,
            ElementType.ANY,
            ElementType.OMNI,
        ], "Element type should only be one of the 7 elements"

        return v

    def __str__(self):
        return f"<{self.id}: {get_display_text(self.name)} [{get_display_text(self.element_type.name)}]>"

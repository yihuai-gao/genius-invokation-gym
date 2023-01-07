"""
Basic character card classes
"""
from abc import abstractmethod
from queue import PriorityQueue
import re
from collections import defaultdict
from typing import TYPE_CHECKING, Optional, Type

from pydantic import BaseModel, Field, validator

from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import Message, UseSkillMsg
from gisim.env import get_display_text

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity

_DEFAULT_SKILL_REGEXPS = {
    # Deals 8 Pyro DMG
    "DMG": r"^deals (\d+) ([a-z]+) dmg$",
    # deals 1 piercing dmg to all opposing characters on standby
    "DMGAll": r"^deals (\d+) ([a-z]+) dmg to all opposing characters on standby$",
    # This character gains Pyro Infusion
    "Inufsion": r"^this character gains ([a-z]+) (elemental )?infusion$",
    # heals this character for 2 hp
    "Heal": r"^heals this character for (\d+) hp$",
    # heals all of your characters for 4 hp
    "HealAll": r"^heals all of your characters for (\d+) hp$",
    # summons 1 shadowsword: galloping frost
    "Summon": r"^summons (\d+) ([a-z: -]+)$",
    # creates 1 pyronado
    "Create": r"^creates (\d+) ([a-z: -]+)$",
    # this character gains niwabi enshou
    "Buff": r"^this character gains ([a-z: -]+)$",
}


class CharacterSkill(BaseModel):
    id: int
    name: str
    text: str
    costs: dict[ElementType, int]
    types: list[SkillType] = Field(..., min_items=1, max_items=1)
    resource: Optional[str] = None  # 图片链接


    @abstractmethod
    def use_skill(self, msg_queue:PriorityQueue[Message], parent:"CharacterEntity"):
        """
        Called when the skill is activated, by default, it parses the skill text and
        returns a list of messages to be sent to the game
        """
        ...

    # def on_skill(self, msg: UseSkillMsg) -> None:
    
    #     for skill in self.parse_skill_text():
    #         # TODO: Send the message to the game
    #         # msg.game.send_message(skill)
    #         pass

    # def _build_message(self, skill_type, *args, **kwargs):
    #     """
    #     Build message here
    #     """

    #     # TODO: This is just a placeholder, need to be implemented

    #     if skill_type == "Unknown":
    #         raise NotImplementedError(
    #             f"You need to override {self}'s `on_skill` or `parse_sub_command` method to handle: \n    {get_display_text(kwargs['command'])}"
    #         )

    #     return dict(type=skill_type, args=args, kwargs=kwargs)

    # def parse_sub_command(self, sub_command: str, full_command: str) -> dict:
    #     for skill_type, regexp in _DEFAULT_SKILL_REGEXPS.items():
    #         results = re.findall(regexp, sub_command)
    #         if results:
    #             return self._build_message(skill_type, tuple(results))

    #     return self._build_message("Unknown", command=full_command)

    # def parse_skill_text(self):
    #     """
    #     Parse the skill text and execute the skill effect
    #     """

    #     text = self.text.lower().replace("</color>", "")

    #     # Use regexp to replace all the color tags
    #     text = re.sub(r"<color=#([0-9a-fA-F]{8})>", "", text)

    #     messages = []
    #     for command in text.split("."):
    #         command = command.strip()
    #         if not command:
    #             continue

    #         # A command is parsable if all of its sub-commands are parsable
    #         for sub_command in command.split(", "):
    #             messages.append(
    #                 self.parse_sub_command(sub_command, full_command=command)
    #             )

    #     return messages

    # def __str__(self):
    #     return f"<{self.id}: {get_display_text(self.name)}>"


class CharacterCard(BaseModel):
    id: int
    name: str
    element_type: ElementType
    nations: list[Nation] = Field(..., min_items=1, max_items=3)  # 所属地区/阵营
    health_point: int = 10
    skills: list[CharacterSkill]
    resource: Optional[str] = None  # 图片链接
    power: int = 0
    max_power: int
    weapon_type: WeaponType
    
    def get_skill(self, id:Optional[int]=None, skill_name:Optional[str]=None, skill_type:Optional[SkillType]=None):
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
            skill_types = [skill.types[0] for skill in self.skills]
            assert (skill_type in skill_types), f"Skill type {skill_type} does not exist."
            assert skill_types.count(skill_type) == 1, f"Skill type {skill_type} is not unique."
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


CHARACTER_CARDS: dict[int, CharacterCard] = {}
CHARACTER_SKILLS: dict[int, CharacterSkill] = {}
CHARACTER_SKILL_FACTORIES: dict[int, Type[CharacterSkill]] = defaultdict(
    lambda: CharacterSkill
)
CHARACTER_NAME2ID: dict[str, int] = {}


def register_character_card(card: CharacterCard, override: bool = False):
    if override is False and card.id in CHARACTER_CARDS:
        raise ValueError(
            f"Character card {card.id} already exists, use override=True to override it, or use silent=True to silence this warning"
        )

    CHARACTER_CARDS[card.id] = card
    CHARACTER_NAME2ID[card.name] = card.id


def register_character_skill(skill: CharacterSkill, override: bool = False):
    if override is False and skill.id in CHARACTER_SKILLS:
        raise ValueError(
            f"Character skill {skill.id} already exists, use override=True to override it, or use silent=True to silence this warning"
        )

    CHARACTER_SKILLS[skill.id] = skill


def register_character_skill_factory(
    skill_id: int,
):
    if skill_id in CHARACTER_SKILL_FACTORIES:
        raise ValueError(f"Character skill factory of skill {skill_id} already exists")

    def decorator(skill_factory: Type[CharacterSkill]):
        CHARACTER_SKILL_FACTORIES[skill_id] = skill_factory
        return skill_factory

    return decorator

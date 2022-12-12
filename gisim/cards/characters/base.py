"""
Basic character card classes
"""
import re
from typing import Any, Optional

from pydantic import BaseModel, Field, validator

from gisim.classes.enums import ElementType, Nation, SkillType

_DEFAULT_SKILL_REGEXPS = {
    # Deals 8 Pyro DMG
    "DMG": r"^deals (\d+) ([a-z]+) dmg$",
    # This character gains Pyro Infusion
    "Inufsion": r"^this character gains ([a-z]+) (elemental )?infusion$",
    # heals this character for 2 hp
    "Heal": r"^heals this character for (\d+) hp$",
    # heals all of your characters for 4 hp
    "HealAll": r"^heals all of your characters for (\d+) hp$",
}


class CharacterSkill(BaseModel):
    id: int
    name: str
    text: str
    costs: dict[ElementType, int]
    types: list[SkillType] = Field(..., min_items=1, max_items=1)
    resource: Optional[str] = None  # 图片链接

    def on_skill(self) -> list:
        """
        Called when the skill is activated, by default, it parses the skill text and
        returns a list of messages to be sent to the game
        """

        return self.parse_skill_text()

    def _build_message(self, skill_type, *args, **kwargs):
        """
        Build message here
        """

        # TODO: This is just a placeholder, need to be implemented

        if skill_type == "Unknown":
            raise NotImplementedError(
                f"You need to override {self.name}'s on_skill method to handle the skill text: \n    {kwargs['command']}"
            )

        return dict(type=skill_type, args=args, kwargs=kwargs)

    def parse_skill_text(self) -> None:
        """
        Parse the skill text and execute the skill effect
        """

        text = self.text.lower().replace("</color>", "")

        # Use regexp to replace all the color tags
        text = re.sub(r"<color=#([0-9a-fA-F]{8})>", "", text)

        messages = []
        for command in text.split("."):
            command = command.strip()
            if not command:
                continue

            for skill_type, regexp in _DEFAULT_SKILL_REGEXPS.items():
                results = re.findall(regexp, command)
                if results:
                    messages.append(self._build_message(skill_type, tuple(results)))
                    break
            else:
                messages.append(self._build_message("Unknown", command=command))

        return messages


class CharacterCard(BaseModel):
    id: int
    name: str
    element_type: ElementType
    nations: list[Nation] = Field(..., min_items=1, max_items=3)  # 所属地区/阵营
    health_point: int = 10
    skills: list[CharacterSkill]
    resource: Optional[str] = None  # 图片链接

    @validator("element_type")
    def element_type_validator(cls, v):
        assert v not in [
            ElementType.POWER,
            ElementType.SAME,
            ElementType.ANY,
        ], "Element type should only be one of the 7 elements"

        return v


CHARACTER_CARDS: dict[int:CharacterCard] = {}
CHARACTER_SKILLS: dict[int:CharacterSkill] = {}


def register_character_card(
    card: CharacterCard, override: bool = False, silent: bool = False
):
    if override is False and card.id in CHARACTER_CARDS and silent is False:
        raise ValueError(
            f"Character card {card.id} already exists, use override=True to override it, or use silent=True to silence this warning"
        )

    CHARACTER_CARDS[card.id] = card


def register_character_skill(
    skill: CharacterSkill, override: bool = False, silent: bool = False
):
    if override is False and skill.id in CHARACTER_SKILLS and silent is False:
        raise ValueError(
            f"Character skill {skill.id} already exists, use override=True to override it, or use silent=True to silence this warning"
        )

    CHARACTER_SKILLS[skill.id] = skill

"""
Basic character card classes
"""
import re
from collections import defaultdict
from typing import Optional, Type

from pydantic import BaseModel, Field, validator

from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType
from gisim.classes.message import Message, MessageReceiver, UseSkillMsg
from gisim.env import get_display_text

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


class CharacterSkill(BaseModel, MessageReceiver):
    id: int
    name: str
    text: str
    costs: dict[ElementType, int]
    types: list[SkillType] = Field(..., min_items=1, max_items=1)
    resource: Optional[str] = None  # 图片链接

    def on_message(self, msg: Message):
        if isinstance(msg, UseSkillMsg):
            self.on_skill(msg)

    def on_skill(self, msg: UseSkillMsg) -> None:
        """
        Called when the skill is activated, by default, it parses the skill text and
        returns a list of messages to be sent to the game
        """

        for skill in self.parse_skill_text():
            # TODO: Send the message to the game
            # msg.game.send_message(skill)
            pass

    def _build_message(self, skill_type, *args, **kwargs):
        """
        Build message here
        """

        # TODO: This is just a placeholder, need to be implemented

        if skill_type == "Unknown":
            raise NotImplementedError(
                f"You need to override {self}'s `on_skill` or `parse_sub_command` method to handle: \n    {get_display_text(kwargs['command'])}"
            )

        return dict(type=skill_type, args=args, kwargs=kwargs)

    def parse_sub_command(self, sub_command: str, full_command: str) -> dict:
        for skill_type, regexp in _DEFAULT_SKILL_REGEXPS.items():
            results = re.findall(regexp, sub_command)
            if results:
                return self._build_message(skill_type, tuple(results))

        return self._build_message("Unknown", command=full_command)

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

            # A command is parsable if all of its sub-commands are parsable
            for sub_command in command.split(", "):
                messages.append(
                    self.parse_sub_command(sub_command, full_command=command)
                )

        return messages

    def __str__(self):
        return f"<{self.id}: {get_display_text(self.name)}>"


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

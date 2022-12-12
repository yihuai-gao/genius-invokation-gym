"""
Basic character card classes
"""

from typing import Optional

from pydantic import BaseModel, Field, validator

from gisim.classes.enums import ElementType, Nation, SkillType


class CharacterSkill(BaseModel):
    id: int
    name: str
    text: str
    costs: dict[ElementType, int]
    types: list[SkillType] = Field(..., min_items=1, max_items=1)
    resource: Optional[str] = None  # 图片链接


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

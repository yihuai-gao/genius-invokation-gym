"""
This files will generate character cards from "gisim/cards/resources/cards_20221205_en-us.json"
"""

import json
import os

from gisim.classes.enums import ElementType, Nation, SkillType

from .base import (
    CHARACTER_SKILL_FACTORIES,
    CHARACTER_SKILLS,
    CharacterCard,
    register_character_card,
    register_character_skill,
)

_ELEMENT_TYPE_MAP = {
    "ETIce": ElementType.CRYO,
    "ETWater": ElementType.HYDRO,
    "ETFire": ElementType.PYRO,
    "ETThunder": ElementType.ELECTRO,
    "ETRock": ElementType.GEO,
    "ETGrass": ElementType.DENDRO,
    "ETWind": ElementType.ANEMO,
}

_NATION_MAP = {
    "Mondstadt": Nation.Mondstadt,
    "Liyue": Nation.Liyue,
    "Inazuma": Nation.Inazuma,
    "Sumeru": Nation.Sumeru,
    "Monster": Nation.Monster,
    "Fatui": Nation.Fatui,
    "Hilichurl": Nation.Hilichurl,
}

_SKILL_TYPE_MAP = {
    "Normal Attack": SkillType.NORMAL_ATTACK,
    "Elemental Skill": SkillType.ELEMENTAL_SKILL,
    "Elemental Burst": SkillType.ELEMENTAL_BURST,
    "Passive Skill": SkillType.PASSIVE_SKILL,
}

_SKILL_COST_MAP = {
    "1": ElementType.POWER,
    "10": ElementType.ANY,
    "11": ElementType.CRYO,
    "12": ElementType.HYDRO,
    "13": ElementType.PYRO,
    "14": ElementType.ELECTRO,
    "15": ElementType.GEO,
    "16": ElementType.DENDRO,
    "17": ElementType.ANEMO,
}


def _process_card(config: dict):
    for skill in config["role_skill_infos"]:
        skill_id = int(skill["id"])

        skill_instance = CHARACTER_SKILL_FACTORIES[skill_id](
            id=skill_id,
            name=skill["name"],
            types=[_SKILL_TYPE_MAP[i] for i in skill["type"] if i],
            text=skill["skill_text"],
            costs={
                _SKILL_COST_MAP[j["cost_icon"]]: int(j["cost_num"])
                for j in skill["skill_costs"]
                if j["cost_icon"]
            },
            resource=skill["resource"],
        )

        register_character_skill(skill_instance, override=False)

    skills = [CHARACTER_SKILLS[int(i["id"])] for i in config["role_skill_infos"]]
    card = CharacterCard(
        id=int(config["id"]),
        name=config["name"],
        nations=[_NATION_MAP[i] for i in config["belong_to"] if i],
        element_type=_ELEMENT_TYPE_MAP[config["element_type"]],
        health_point=int(config["hp"]),
        resource=config["resource"],
        skills=skills,
        max_power=max([skill.costs[ElementType.POWER] for skill in skills if ElementType.POWER in skill.costs.keys()])
    )

    register_character_card(card, override=False)


def generate_character_cards_and_skills():
    path = os.path.join(
        os.path.dirname(__file__), "..", "resources", "cards_20221205_en-us.json"
    )

    with open(path, "r") as f:
        cards = json.load(f)["role_card_infos"]

    for i in cards:
        _process_card(i)

"""
This files will generate character cards from "gisim/cards/resources/cards_20221205_en-us.json"
"""

from collections import defaultdict
import json
import os
import re
from typing import Type
from gisim.cards.characters.base import CharacterCard, CharacterSkill

from gisim.classes.enums import ElementType, Nation, SkillType, WeaponType


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

_WEAPON_TYPE_MAP = {
    "Bow": WeaponType.BOW,
    "Sword": WeaponType.SWORD,
    "Claymore": WeaponType.CLAYMORE,
    "Polearm": WeaponType.POLEARM,
    "Catalyst": WeaponType.CATALYST,
    "Other Weapons": WeaponType.OTHER_WEAPONS,
}


def _process_card(config: dict):
    for skill in config["role_skill_infos"]:
        skill_id = int(skill["id"])
        text = skill["skill_text"]
        text = text.replace("</color>", "")

        # Use regexp to replace all the color tags
        text = re.sub(r"<color=#([0-9a-fA-F]{8})>", "", text)
        skill_instance = CHARACTER_SKILL_FACTORIES[skill_id](
            id=skill_id,
            name=skill["name"],
            type=[_SKILL_TYPE_MAP[i] for i in skill["type"] if i][0],
            text=text,
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
        max_power=max(
            [
                skill.costs[ElementType.POWER]
                for skill in skills
                if ElementType.POWER in skill.costs.keys()
            ]
        ),
        weapon_type=_WEAPON_TYPE_MAP[config["weapon"]],
    )

    register_character_card(card, override=False)


def generate_character_cards_and_skills():
    path = os.path.join(
        os.path.dirname(__file__), "..", "gisim", "resources", "cards_20221205_en-us.json"
    )

    with open(path, "r") as f:
        cards = json.load(f)["role_card_infos"]

    for i in cards:
        _process_card(i)

def parse_sub_command(sub_command: str):
    for skill_type, regexp in _DEFAULT_SKILL_REGEXPS.items():
        results = re.findall(regexp, sub_command)
        if results:
            return [skill_type, results]
    return [sub_command]


def parse_skill_text(text):
    """
    Parse the skill text and execute the skill effect
    """

    effects = []
    for command in text.split("."):
        command = command.strip()
        if not command:
            continue

        # A command is parsable if all of its sub-commands are parsable
        for sub_command in command.split(", "):
            effects.append(
                parse_sub_command(sub_command)
            )

    return effects

if __name__ == "__main__":
    generate_character_cards_and_skills()
    character_name = "Collei"
    character_card = CHARACTER_CARDS[CHARACTER_NAME2ID[character_name]]
    print(f"Name: {character_card.name}, Nations: {character_card.nations}, Weapon: {character_card.weapon_type}, Element: {character_card.element_type}")
    skills = character_card.skills
    print("Skills:")
    for skill in skills:
        print(f"    Name: {skill.name}, type: {skill.type}, cost: {skill.costs}, text: {skill.text}")
        effects = parse_skill_text(skill.text)
        for effect in effects:
            print(f"          {effect}")
        

import json
import os
import re

from classes.enums import ElementType


def strip_content(content: str):
    content = content.replace("</color>", "").replace("\\n", "")
    # Use regexp to replace all the color tags
    content = re.sub(r"<color=#([0-9a-fA-F]{8})>", "", content)
    return content


def get_equipments(equipment_type: str):
    path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "gisim",
        "resources",
        "cards_20221205_en-us.json",
    )

    with open(path, "r") as f:
        cards = json.load(f)["action_card_infos"]

    equipments = []
    for card in cards:
        if (
            card["action_type"] == "AcEquip"
            and card["action_card_tags"][0]["text"] == equipment_type
        ):
            card["content"] = strip_content(card["content"])
            equipments.append(card)
    print(len(equipments))
    return equipments


_WEAPON_COST_MAP = {
    "3": ElementType.SAME,
    "10": ElementType.ANY,
}


def print_weapon(weapon):
    costs = {}
    costs[_WEAPON_COST_MAP[weapon["cost_type1_icon"]]] = int(weapon["cost_num1"])
    if weapon["cost_num2"]:
        costs[_WEAPON_COST_MAP[weapon["cost_type2_icon"]]] = int(weapon["cost_num2"])
    cost_str = ""
    for elem, val in costs.items():
        cost_str += f"ElementType.{elem}: {val}"
    cost_str = "{" + cost_str + "}"
    weapon_str = weapon["name"].replace(" ", "").replace("'", "")
    weapon_type_str: str = weapon["action_card_tags"][1]["text"]
    print(
        f'''
class {weapon_str}Card(WeaponCard):
    id: int = {weapon['id']}
    name: str = "{weapon['name']}"
    text: str = """{weapon['content']}"""
    costs: Dict[ElementType, int] = {cost_str}
    weapon_type: WeaponType = WeaponType.{weapon_type_str.upper()}

class {weapon_str}(WeaponEntity):
    id: int = {weapon['id']}
    name: str = "{weapon['name']}"
    weapon_type: WeaponType = WeaponType.{weapon_type_str.upper()}
'''
    )


if __name__ == "__main__":
    weapons = get_equipments("Weapon")
    for weapon in weapons:
        print_weapon(weapon)

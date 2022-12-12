"""神里绫华"""
from mailbox import NotEmptyError

from classes import Character, Skill, Summon
from global_config import DISPLAY_LANGUAGE

from gisim.classes.enums import *


class KamisatoAyaka(Character):
    """神里绫华"""

    def __init__(self, player_id: PlayerID, position: Position):
        if DISPLAY_LANGUAGE == "Chinese":
            super().__init__("神里绫华", player_id, position)
            self.SKILL_NAMES = ["神里流·倾", "神里流·冰华", "神里流·霜灭", "神里流·霰步"]
            self.NATIONALITY = "稻妻"
            self.WEAPON_TYPE = "单手剑"
        elif DISPLAY_LANGUAGE == "English":
            super().__init__("KamisatoAyaka", player_id, position)
            self.SKILL_NAMES = [
                "Kamisato Art: Kabuki",
                "Kamisato Art: Hyouka",
                "Kamisato Art: Soumetsu",
                "Kamisato Art: Senho",
            ]
            self.NATIONALITY = "Inazuma"
            self.WEAPON_TYPE = "sword"
        self.health_point = 10
        self.SKILL_NUM = 4
        # Init skills

        normal_attack = Skill(
            name=self.SKILL_NAMES[0],
            cost={ET.CRYO: 1, ET.UNALIGNED: 2},
            skill_type=ST.NORMAL_ATTACK,
        )

        elemental_skill = Skill(
            name=self.SKILL_NAMES[1], cost={ET.CRYO: 3}, skill_type=ST.ELEMENTAL_SKILL
        )

        elemental_burst = Skill(
            name=self.SKILL_NAMES[2],
            cost={ET.CRYO: 3, ET.POWRE: 3},
            skill_type=ST.ELEMENTAL_BURST,
        )

        passive_skill = Skill(
            name=self.SKILL_NAMES[3], cost=None, skill_type=ST.PASSIVE_SKILL
        )

        self.skills = [normal_attack, elemental_skill, elemental_burst, passive_skill]

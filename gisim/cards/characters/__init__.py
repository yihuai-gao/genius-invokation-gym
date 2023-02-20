# Load all overrides
from typing import TypeVar

from gisim.classes.enums import PlayerID

from .Anemo import *
from .Cryo import *
from .Dendro import *
from .Electro import *
from .Geo import *
from .Hydro import *
from .Pyro import *

# Make isort happy
...

# Generate character cards and skills from the game data
# from .base import CHARACTER_CARDS, CHARACTER_NAME2ID, CHARACTER_SKILLS
# from .generator import generate_character_cards_and_skills

# generate_character_cards_and_skills()

# __all__ = ["CHARACTER_CARDS", "CHARACTER_SKILLS", "CHARACTER_NAME2ID"]
def get_character_card(character_name: str):
    # TODO: Is there any better ways to do this?
    character_name = character_name.replace(" ", "").replace("'", "")
    # character_card: CharacterCard = eval(f"{character_name}()")
    character_card_class = globals()[character_name]
    # Remove the spaces for class names
    return character_card_class()


def get_skill_type(skill_name: str):
    skill_name = skill_name.replace(" ", "").replace("'", "")
    skill_class = globals()[skill_name]
    skill:CharacterSkill = skill_class()
    return skill.type
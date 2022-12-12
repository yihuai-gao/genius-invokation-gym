# Load all overrides
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
from .base import CHARACTER_CARDS, CHARACTER_NAME2ID, CHARACTER_SKILLS
from .generator import generate_character_cards_and_skills

generate_character_cards_and_skills()

__all__ = ["CHARACTER_CARDS", "CHARACTER_SKILLS", "CHARACTER_NAME2ID"]

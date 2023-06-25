from ..cards import get_character_status as get_cards_character_status
from ..cards import get_combat_status as get_cards_combat_status

# Files need to be reorganized
from .dendro_reaction import *
from .frozen_effect import *
from .shield import *


def get_combat_status(status_name: str):
    status_name = status_name.replace(" ", "").replace("'", "")
    if not status_name.endswith("Status"):
        status_name += "Status"
    if status_name in globals():
        status_class = globals()[status_name]
        status: CombatStatusEntity = status_class()
        return status
    else:
        return get_cards_combat_status(status_name)


def get_character_status(status_name: str):
    status_name = status_name.replace(" ", "").replace("'", "")
    if not status_name.endswith("Status"):
        status_name += "Status"
    status_class = globals()[status_name]
    status: CharacterStatusEntity = status_class()
    return status

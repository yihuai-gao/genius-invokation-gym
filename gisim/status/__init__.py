from typing import cast

### import other status from card files
from gisim.cards import get_character_status as import_cards_character_status
from gisim.cards import get_combat_status as import_cards_combat_status
from gisim.classes.enums import CharPos, ElementType, PlayerID
from gisim.classes.status import CharacterStatusEntity, CombatStatusEntity
from gisim.env import INF_INT

from .reaction_status import *

###


def get_combat_status(
    name: str, player_id: PlayerID, position: CharPos, remaining_round: int
):
    name = name.replace(" ", "").replace("'", "")
    if not name.endswith("Status"):
        name += "Status"
    if name in globals():
        status_class = globals()[name]
        status: CombatStatusEntity = status_class(
            player_id=player_id, position=position, remaining_round=remaining_round
        )
        return status
    else:
        return import_cards_combat_status(name, player_id, position, remaining_round)


def get_character_status(
    name: str, player_id: PlayerID, position: CharPos, remaining_round: int
):
    name = name.replace(" ", "")
    if not name.endswith("Status"):
        name += "Status"
    if name.endswith("InfusionStatus"):
        elem_char = name.replace("InfusionStatus", "").upper()
        element: ElementType = eval(f"ElementType.{elem_char}")
        status = ElementalInfusionStatus(
            name=name,
            player_id=player_id,
            position=position,
            remaining_round=remaining_round,
            element=element,
        )
        status = cast(CharacterStatusEntity, status)
        return status

    if name in globals():
        status_class = globals()[name]
        status: CharacterStatusEntity = status_class(
            player_id=player_id, position=position, remaining_round=remaining_round
        )
        return status

    else:
        return import_cards_character_status(name, player_id, position, remaining_round)

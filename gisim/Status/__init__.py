# from .FrozenEffect import *
from typing import cast

from gisim.classes.enums import CharPos, ElementType, PlayerID
from gisim.status.base import CharacterStatusEntity
from gisim.status.characterStatus import *
from gisim.status.reactionStatus import *


def get_character_status_entity(
    name: str, player_id: PlayerID, position: CharPos, remaining_round: int
):
    stripped_name = name.replace(" ", "")
    if stripped_name.endswith("Infusion"):
        elem_char = stripped_name.replace("Infusion", "").upper()
        element: ElementType = eval(f"ElementType.{elem_char}")
        status = ElementalInfusion(
            name=name,
            player_id=player_id,
            position=position,
            remaining_round=remaining_round,
            element=element,
        )
        status = cast(CharacterStatusEntity, status)
        return status

    status_cls = globals()[stripped_name]
    status: CharacterStatusEntity = status_cls(
        player_id=player_id, position=position, remaining_round=remaining_round
    )
    return status

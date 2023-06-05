# from .FrozenEffect import *
from typing import cast

from gisim.classes.enums import CharPos, ElementType, PlayerID, StatusType
from gisim.env import INF_INT
from gisim.status.base import CharacterStatusEntity, CombatStatusEntity
from gisim.status.character_status import *
from gisim.status.combat_status import get_combat_status_entity
from gisim.status.reaction_status import *


def get_character_status_entity(
    name: str,
    player_id: PlayerID,
    position: CharPos,
    buff_type: StatusType,
    remaining_round: int,
    remaining_usage: int,
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
            remaining_usage=remaining_usage,
            element=element,
            status_type=buff_type,
        )
        status = cast(CharacterStatusEntity, status)
        return status

    status_cls = globals()[stripped_name]
    status: CharacterStatusEntity = status_cls(
        player_id=player_id,
        position=position,
        remaining_round=remaining_round,
        remaining_usage=remaining_usage,
        status_type=buff_type,
    )
    return status

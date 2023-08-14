from typing import Optional, Tuple, Type

from gisim.cards.base import Card
from gisim.cards.characters import *
from gisim.cards.equipments import *
from gisim.cards.events import *
from gisim.cards.supports import *
from gisim.classes.equipment import EquipmentEntity

# There might be some better ways to register all the classes into a dictionary

CLASS_ID_REGISTER = {
    entity_cls.__fields__["id"].default: entity_cls
    for entity_cls in globals().values()
    if hasattr(entity_cls, "__fields__") and "id" in entity_cls.__fields__.keys()
}


def search_class_by_id(class_id: int, class_name: Type):
    entity_cls = CLASS_ID_REGISTER[class_id]
    if issubclass(entity_cls, class_name):
        return entity_cls
    raise (KeyError(f"Cannot find entity of type {class_name} with id {class_id}"))


def get_summon_entity(
    player_id: PlayerID,
    summon_id: Optional[int] = None,
    summon_name: Optional[str] = None,
):
    if summon_id is not None:
        summon_class = search_class_by_id(summon_id, Summon)
    elif summon_name is not None:
        summon_name = summon_name.replace(" ", "").replace("'", "")
        summon_class = globals()[summon_name]
    else:
        raise (ValueError("Either summon_id or summon_name should be provided."))
    summon: Summon = summon_class(player_id=player_id)
    return summon


def get_card(card_name: str):
    card_name = card_name.replace(" ", "").replace("'", "") + "Card"
    card_class = globals()[card_name]
    card: Card = card_class()
    return card


def get_equipment(equipment_name: str, target: Tuple[PlayerID, CharPos]):
    equipment_name = equipment_name.replace(" ", "").replace("'", "")
    equipment_class = globals()[equipment_name]
    equipment: EquipmentEntity = equipment_class(
        player_id=target[0], char_pos=target[1]
    )
    return equipment


def get_combat_status(
    player_id: PlayerID,
    remaining_round: int,
    status_id: Optional[int] = None,
    status_name: Optional[str] = None,
):
    if status_id is not None:
        status_class = search_class_by_id(status_id, CombatStatusEntity)
    elif status_name is not None:
        status_name = status_name.replace(" ", "").replace("'", "")
        if not status_name.endswith("Status"):
            status_name += "Status"
        status_class = globals()[status_name]
    else:
        raise (ValueError("Either status_id or status_name should be provided."))

    status: CombatStatusEntity = status_class(
        player_id=player_id, remaining_round=remaining_round
    )
    return status


def get_character_status(
    player_id: PlayerID,
    position: CharPos,
    remaining_round: int,
    status_id: Optional[int] = None,
    status_name: Optional[str] = None,
):
    if status_id is not None:
        status_class = search_class_by_id(status_id, CharacterStatusEntity)
    elif status_name is not None:
        status_name = status_name.replace(" ", "").replace("'", "")
        if not status_name.endswith("Status"):
            status_name += "Status"
        status_class = globals()[status_name]
    else:
        raise (ValueError("Either status_id or status_name should be provided."))

    status: CharacterStatusEntity = status_class(
        player_id=player_id, position=position, remaining_round=remaining_round
    )
    return status

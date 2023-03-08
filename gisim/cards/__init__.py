from typing import Tuple
from gisim.cards.base import Card
from gisim.cards.characters import *
from gisim.cards.equipments import *
from gisim.cards.events import *
from gisim.cards.supports import *
from gisim.classes.equipment import EquipmentEntity

# from .characters import CHARACTER_CARDS, CHARACTER_SKILLS


def get_summon_entity(summon_name: str, player_id: PlayerID):
    summon_name = summon_name.replace(" ", "").replace("'", "")
    summon_class = globals()[summon_name]
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

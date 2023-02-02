from gisim.cards.base import Card
from gisim.cards.equipments import *
from gisim.cards.events import *
from gisim.cards.characters import *
from gisim.cards.supports import *
# from .characters import CHARACTER_CARDS, CHARACTER_SKILLS


def get_summon_entity(summon_name: str, player_id: PlayerID):
    summon_name = summon_name.replace(" ", "")
    summon_class = globals()[summon_name]
    summon: Summon = summon_class(player_id=player_id)
    return summon

def get_card(card_name: str):
    card_name = card_name.replace(" ", "")+"Card"
    card_class = globals()[card_name]
    card:Card = card_class()
    return card
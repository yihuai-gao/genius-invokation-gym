from gisim.classes.enums import PlayerID
from gisim.env import INF_INT
from gisim.classes.status import CombatStatusEntity

from .Chongyun import *
from .dendro_reaction import *
from .Shield import *
from .Xingqiu import *


def get_combat_status_entity(
    name: str, player_id: PlayerID, remaining_round: int, remaining_usage: int = INF_INT
):
    stripped_name = name.replace(" ", "")
    status_cls = globals()[stripped_name]
    status: CombatStatusEntity = status_cls(
        player_id=player_id,
        remaining_round=remaining_round,
        remaining_usage=remaining_usage,
    )
    return status

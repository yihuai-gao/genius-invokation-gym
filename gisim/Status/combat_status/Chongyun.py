from queue import PriorityQueue

from gisim.env import INF_INT
from gisim.status import CombatStatusEntity


class ChonghuasFrostField(CombatStatusEntity):
    """Combat Statu: Chonghua's Frost Field
    Your Sword, Claymore, and Polearm-wielding characters' Physical DMG is converted to Cryo DMG.
    Duration (Rounds): 2
    """

    name: str = "Chonghuas Frost Field"
    description: str = """Your Sword, Claymore, and Polearm-wielding characters' Physical DMG is converted to Cryo DMG.Duration (Rounds): 2"""
    active: bool = True
    value: int = 0
    remaining_round: int = 2
    remaining_usage: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        # TODO: Get Sword, Claymore, Polearm-wielding Character.
        return False

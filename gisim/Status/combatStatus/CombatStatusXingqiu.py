from gisim.status.base import CombatStatusEntity
from queue import PriorityQueue
from gisim.classes.message import (
    DealDamageMsg,
    RoundEndMsg
)
from gisim.env import INF_INT


class RainSword(CombatStatusEntity):
    """[Combat Status]When your active character receives at least 3 DMG: 
    Decrease DMG taken by 1.
    Usage(s): 2
    """
    name: str = "Rain Sword"
    description: str = """When your active character receives at least 3 DMG: Decrease DMG taken by 1.Usage(s): 2"""
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 2
    

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        if isinstance(top_msg, DealDamageMsg):
            pass
        return False


class RainbowBladework(CombatStatusEntity):
    """[Combat Status]After your character uses a Normal Attack: 
    Deal 1 Hydro DMG.
    Usage(s): 3"""
    name = "Rainbow Bladework"
    description = "After your character uses a Normal Attack: Deal 1 Hydro DMG.Usage(s): 3"
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 3

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        # print(f"Add Combat Status: {self.description}")
        return False

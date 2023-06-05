from queue import PriorityQueue
from typing import cast

from gisim.classes.enums import *
from gisim.classes.message import DealDamageMsg, RoundEndMsg
from gisim.env import INF_INT
from gisim.status.base import CombatStatusEntity


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
            top_msg = cast(DealDamageMsg, top_msg)

            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                top_msg.targets
            ):
                if target_id == self.player_id:
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val - 1 if dmg_val >= 3 else dmg_val,
                    )
                    self.remaining_usage -= 1
            if self.remaining_usage == 0 or self.remaining_round == 0:
                self.active = False

        return False


class RainbowBladework(CombatStatusEntity):
    """[Combat Status]After your character uses a Normal Attack:
    Deal 1 Hydro DMG.
    Usage(s): 3"""

    name = "Rainbow Bladework"
    description = (
        "After your character uses a Normal Attack: Deal 1 Hydro DMG.Usage(s): 3"
    )
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 3

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        # print(f"Add Combat Status: {self.description}")
        return False

from queue import PriorityQueue
from typing import cast

from gisim.classes.enums import *
from gisim.classes.message import DealDamageMsg, RoundEndMsg
from gisim.env import INF_INT
from gisim.status.base import CharacterStatusEntity


class ElementalInfusion(CharacterStatusEntity):
    name: str
    element: ElementType
    description: str = "Convert physical damage into elemental damage"
    value: int = 0
    active: bool = True
    remaining_usage: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attacker == (self.player_id, self.position):
                for idx, target in enumerate(top_msg.targets):
                    if target[2] == ElementType.NONE:
                        print(
                            f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {target[2]} -> {target[3]} + Add: 0\n        {self.player_id.name}-{self.position}\n"
                        )
                        top_msg.targets[idx] = (
                            target[0],
                            target[1],
                            self.element,
                            target[3],
                        )
                        updated = True

        if isinstance(top_msg, RoundEndMsg):
            top_msg = cast(RoundEndMsg, top_msg)
            assert (
                self.remaining_round >= 1
            ), "Remaining round should not be lower than 1!"
            self.remaining_round -= 1
            if self.remaining_round == 0:
                self.active = False
        if updated:
            top_msg.responded_entities.append(self._uuid)
        return updated

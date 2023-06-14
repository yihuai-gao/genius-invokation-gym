from queue import PriorityQueue
from typing import cast

from gisim.classes.message import DealDamageMsg
from gisim.env import INF_INT
from gisim.classes.status import CombatStatusEntity


class Shield(CombatStatusEntity):
    """Shield"""

    name: str = "Shield"
    description: str = "Shield"
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        updated = False

        if self._uuid in top_msg.responded_entities:
            return False

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)

            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                top_msg.targets
            ):
                if target_id == self.player_id and dmg_val > 0:
                    print(
                        f"    Combat Status Effect By {self.player_id.name}:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} - {1}\n"
                    )
                    after_dmg = max(0, dmg_val - self.remaining_round)
                    # 护盾只能抵消伤害，改挂元素还是得挂元素

                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        after_dmg,
                    )
                    self.remaining_usage = max(0, self.remaining_round - dmg_val)
                    updated = True

        if self.remaining_usage == 0:
            self.active = False
        if updated:
            top_msg.responded_entities.append(self._uuid)

        return updated

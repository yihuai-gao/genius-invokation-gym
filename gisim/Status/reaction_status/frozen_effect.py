from queue import PriorityQueue
from typing import cast

from gisim.classes.enums import *
from gisim.classes.message import DealDamageMsg, RoundEndMsg
from gisim.status.base import CharacterStatusEntity


class FrozenEffect(CharacterStatusEntity):
    """
    [Character Status]the target is unable to perform any Actions this round
    (Can be removed in advance after the target receives Physical or Pyro DMG,
    in which case they will take +2 DMG)
    """

    name: str = "Frozen Effect"
    element: ElementType = ElementType.NONE
    description: str = """[Character Status]the target is unable to perform any Actions this round(Can be removed in advance after the target receives Physical or Pyro DMG, in which case they will take +2 DMG)"""
    value: int = 0
    active: bool = True
    status_type: StatusType = StatusType.UNDER_ATTACK_BUFF
    remaining_usage = 1

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return False

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.damage_calculation_ended:
                return False
            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                top_msg.targets
            ):
                if (
                    target_id == self.player_id
                    and target_pos == self.position
                    and element_type in [ElementType.NONE, ElementType.PYRO]
                ):
                    print(
                        f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} + Add: 2\n        {self.player_id.name}-{self.position}\n"
                    )

                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val + 2,
                    )
                    updated = True
                    self.remaining_usage -= 1

        if isinstance(top_msg, RoundEndMsg):
            self.remaining_round -= 1
            if self.remaining_round == 0:
                self.active = False

        if updated:
            msg_queue.queue[0].responded_entities.append(self._uuid)
        return updated

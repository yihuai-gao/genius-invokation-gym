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

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False

        updated = False
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            # 负面buff 为别人加伤
            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(top_msg.targets):
                if target_id == self.player_id and target_pos == self.position and element_type in [ElementType.NONE, ElementType.PYRO]:
                    print(
                        f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} + Add: 2\n        {self.player_id.name}-{self.position} be subjected to Physical or Pyro DMG")
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val + 2,
                    )
                    updated = True
                    # 冻结时遭受物理攻击或者火元素伤害 冻结撤销
                    self.remaining_round = 0
                    self.active = False

        if isinstance(top_msg, RoundEndMsg):
            # 回合结束冻结 撤销
            self.remaining_round = 0
            self.active = False
        if updated:
            msg_queue.queue[0].responded_entities.append(self._uuid)
        return updated

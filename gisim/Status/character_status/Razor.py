from queue import PriorityQueue
from typing import cast

from gisim.classes.enums import AttackType, ElementType, StatusType
from gisim.classes.message import DealDamageMsg, RoundEndMsg
from gisim.env import INF_INT
from gisim.classes.status import CharacterStatusEntity


class TheWolfWithin(CharacterStatusEntity):
    """Character Status: The Wolf Within
    After the character to which this is attached uses a Normal Attack or an Elemental Skill:
    Deal 2 Electro DMG.
    Duration (Rounds): 2"""

    name: str = "The Wolf Within"
    element: ElementType = ElementType.ELECTRO
    status_type: StatusType = StatusType.ATTACK_BUFF
    description: str = """After the character to which this is attached uses a Normal Attack or an Elemental Skill: Deal 2 Electro DMG.Duration (Rounds): 2"""
    value: int = 0
    active: bool = True
    remaining_round: int = 2
    remaining_usage: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return False

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            attacker_id, attacker_pos = top_msg.attacker
            if (
                attacker_id == self.player_id
                and attacker_pos == self.position
                and top_msg.attack_type
                in [AttackType.NORMAL_ATTACK, AttackType.ELEMENTAL_SKILL]
            ):
                new_msg = DealDamageMsg(
                    sender_id=self.player_id,
                    attack_type=AttackType.COMBAT_STATUS,
                    attacker=(self.player_id, self.position),
                    target_id=[
                        (target_id, target_pos, self.element, 1)
                        for target_id, target_pos, element_type, dmg_val in top_msg.targets
                    ],
                )
                msg_queue.put(new_msg)
                updated = True

        if isinstance(top_msg, RoundEndMsg):
            self.remaining_round -= 1
            if self.remaining_round == 0:
                self.remaining_usage = 0
                self.active = False

        if updated:
            top_msg.responded_entities.append(self._uuid)

        return updated

# Character Status
from gisim.status import CharacterStatusEntity
from queue import PriorityQueue
from typing import  cast

from gisim.classes.enums import AttackType, StatusType
from gisim.env import INF_INT
from gisim.classes.message import DealDamageMsg

class ChakraDesiderata(CharacterStatusEntity):
    """Character Status: Chakra Desiderata
    After your other characters use Elemental Bursts: Gain 1 Resolve. (Max 3)
    When the character to which this is attached uses Secret Art:
    Musou Shinsetsu: Consume all Resolve and deal +1 DMG per Resolve."""

    name: str = "Chakra Desiderata"
    status_type: StatusType = StatusType.ATTACK_BUFF
    max_resolve: int = 3
    resolve: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = INF_INT
    value: int = 0

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            attacker_id, attacker_pos = top_msg.attacker
            # As Raiden Shogun used Elemental Burst
            if (
                attacker_id == self.player_id
                and attacker_pos == self.position
                and top_msg.attack_type == AttackType.ELEMENTAL_BURST
            ):
                for dmg_obj in top_msg.targets:
                    dmg_obj[3] += self.resolve
                self.resolve = 0
                updated = True

            # TODO: use AfterUseSkillMsg is Better?

            # As Other Characters use Elemental Butsts
            if (
                attacker_id == self.player_id
                and attacker_pos is not self.position
                and top_msg.attack_type == AttackType.ELEMENTAL_BURST
            ):
                self.resolve = min(self.max_resolve, self.resolve + 1)
                updated = False
        return updated

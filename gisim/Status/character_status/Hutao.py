from queue import PriorityQueue
from typing import cast

from gisim.classes.enums import *
from gisim.classes.message import DealDamageMsg, RoundEndMsg
from gisim.env import INF_INT
from gisim.status import CharacterStatusEntity


class ParamitaPapilio(CharacterStatusEntity):
    """The character to which this is attached has their Physical DMG dealt converted to Pyro DMG,
    and they will deal +1 Pyro DMG.Some times can Apply [Blood Blossom].
    Duration (Rounds): 2
    """

    name: str = "Paramita Papilio"
    element: ElementType = ElementType.PYRO
    status_type: StatusType = StatusType.ATTACK_BUFF
    description: str = """The character to which this is attached has their Physical DMG dealt converted to Pyro DMG, and they will deal +1 Pyro DMG.Some times can Apply [Blood Blossom].Duration (Rounds): 2"""
    value: int = 0
    active: bool = True

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return False

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attacker == (self.player_id, self.position):
                for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                    top_msg.targets
                ):
                    print(
                        f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} + Add: 1\n        {self.player_id.name}-{self.position}\n"
                    )
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        self.element
                        if element_type is ElementType.NONE
                        else element_type,
                        dmg_val + 1,
                    )
                    updated = True

        if isinstance(top_msg, RoundEndMsg):
            self.remaining_round -= 1

            if self.remaining_round == 0:
                self.remaining_usage = 0
                self.active = False

        # TODO Charged Attack: Apply Blood Blossom to target character.

        if updated:
            msg_queue.queue[0].responded_entities.append(self._uuid)

        return updated


class BloodBlossom(CharacterStatusEntity):
    """End Phase: Deal 1 Pyro DMG to the character to which this is attached.
    Usage(s): 1
    """

    name: str = "Paramita Papilio"
    element: ElementType = ElementType.PYRO
    status_type: StatusType = StatusType.NEGATIVE_BUFF
    description: str = """End Phase: Deal 1 Pyro DMG to the character to which this is attached. Usage(s): 1"""
    value: int = 0
    active: bool = True
    remaining_round: int = 1
    remaining_usage: int = 1

    def msg_handler(self, msg_queue: PriorityQueue):
        if self._uuid in top_msg.responded_entities:
            return False
        top_msg = msg_queue.queue[0]
        updated = False
        if isinstance(top_msg, RoundEndMsg):
            new_msg = DealDamageMsg(
                sender_id=self.player_id,
                attack_type=AttackType.COMBAT_STATUS,
                attacker=(self.player_id, self.position),
                targets=[(self.player_id, self.position, self.element, 1)],
            )
            msg_queue.put(new_msg)
            updated = True
            self.remaining_usage -= 1
            self.remaining_round -= 1
            self.active = False

        if updated:
            msg_queue.queue[0].responded_entities.append(self._uuid)

        return updated

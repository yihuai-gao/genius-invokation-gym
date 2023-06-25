from queue import PriorityQueue
from typing import cast

from gisim.classes.enums import *
from gisim.classes.message import DealDamageMsg
from gisim.classes.status import CombatStatusEntity
from gisim.env import INF_INT


class DendroCoreStatus(CombatStatusEntity):
    """[Combat Status]When you deal Icon TCG PyroPyro DMG or Icon TCG ElectroElectro DMG to an opposing active character,
    DMG dealt +2. (1 Usage)
    """

    name: str = "Dendro Core"
    description: str = """When you deal Icon TCG PyroPyro DMG or Icon TCG ElectroElectro DMG to an opposing active character, DMG dealt +2. (1 Usage)"""
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 2

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            attacker_id, attacker_pos = top_msg.attacker
            if attacker_id == self.player_id:
                for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                    top_msg.targets
                ):
                    if element_type in [ElementType.PYRO, ElementType.ELECTRO]:
                        print(
                            f"    Combat Status Effect By {self.player_id.name}:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} + {2}\n"
                        )
                        top_msg.targets[idx] = (
                            target_id,
                            target_pos,
                            element_type,
                            dmg_val + 2,
                        )
                    self.remaining_usage -= 1

        if self.remaining_usage == 0 or self.remaining_round == 0:
            self.active = False

        return False


class CatalyzingFieldStatus(CombatStatusEntity):
    """[Combat Status]When you deal Icon TCG ElectroElectro DMG or Icon TCG DendroDendro DMG to an opposing active character,
    DMG dealt +1. (3 Usages)"""

    name: str = "Catalyzing Field"
    description: str = """When you deal Icon TCG ElectroElectro DMG or Icon TCG DendroDendro DMG to an opposing active character, DMG dealt +1. (2 Usages)"""
    active: bool = True
    value: int = 0
    remaining_round: int = INF_INT
    remaining_usage: int = 3

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            attacker_id, attacker_pos = top_msg.attacker
            if attacker_id == self.player_id:
                for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                    top_msg.targets
                ):
                    if element_type in [ElementType.DENDRO, ElementType.ELECTRO]:
                        print(
                            f"    Combat Status Effect By {self.player_id.name}:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} + {2}\n"
                        )
                        top_msg.targets[idx] = (
                            target_id,
                            target_pos,
                            element_type,
                            dmg_val + 1,
                        )
                    self.remaining_usage -= 1

            if self.remaining_usage == 0 or self.remaining_round == 0:
                self.active = False

            return False

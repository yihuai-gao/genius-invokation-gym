"""Base classes of all kinds of equipment: Weapon, Artifact, Talent
"""

from queue import PriorityQueue
from typing import cast

from gisim.classes.entity import Entity
from gisim.classes.enums import (
    CharPos,
    ElementType,
    EquipmentType,
    PlayerID,
    WeaponType,
)
from gisim.classes.message import DealDamageMsg, Message


class EquipmentEntity(Entity):
    name: str
    active: bool = True
    player_id: PlayerID
    char_pos: CharPos
    triggered_in_a_round: int = 0
    """How many times triggered in this round. Might be useful in some entities"""
    equipment_type: EquipmentType

    def encode(self):
        return self.dict().update({"_uuid": self._uuid})


class TalentEntity(EquipmentEntity):
    equipment_type: EquipmentType = EquipmentType.TALENT


class WeaponEntity(EquipmentEntity):
    equipment_type: EquipmentType = EquipmentType.WEAPON
    weapon_type: WeaponType

    def msg_handler(self, msg_queue: PriorityQueue):
        # Increase 1 dmg by default without any advanced effects
        top_msg = msg_queue.queue[0]
        updated = False
        if self._uuid in top_msg.responded_entities:
            return updated

        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attacker == (self.player_id, self.char_pos):
                for idx, (player_id, char_pos, elem_type, dmg_val) in enumerate(
                    top_msg.targets
                ):
                    if elem_type is not ElementType.PIERCE:
                        top_msg.targets[idx] = (
                            player_id,
                            char_pos,
                            elem_type,
                            dmg_val + 1,
                        )
                        updated = True

        if updated:
            top_msg.responded_entities.append(self._uuid)
        return updated


class ArtifactEntity(EquipmentEntity):
    equipment_type: EquipmentType = EquipmentType.ARTIFACT

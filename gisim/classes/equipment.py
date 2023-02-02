"""Base classes of all kinds of equipment: Weapon, Artifact, Talent
"""

from queue import PriorityQueue

from gisim.classes.entity import Entity
from gisim.classes.enums import CharPos, EquipmentType, PlayerID
from gisim.classes.message import Message


class EquipmentEntity(Entity):
    name: str
    active: bool = True
    player_id: PlayerID
    char_pos: CharPos
    triggered_in_a_round: int = 0
    """How many times triggered in this round. Might be useful in some entities"""
    equipment_type: EquipmentType

    def encode(self):
        return self.dict()


class TalentEntity(EquipmentEntity):
    equipment_type: EquipmentType = EquipmentType.TALENT


class WeaponEntity(EquipmentEntity):
    equipment_type: EquipmentType = EquipmentType.WEAPON


class ArtifactEntity(EquipmentEntity):
    equipment_type: EquipmentType = EquipmentType.ARTIFACT

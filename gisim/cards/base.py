from queue import PriorityQueue
from typing import TYPE_CHECKING, cast

from pydantic import BaseModel

from gisim.classes.enums import (
    CardType,
    CharPos,
    ElementType,
    EntityType,
    EquipmentType,
    PlayerID,
    WeaponType,
)
from gisim.classes.message import GenerateEquipmentMsg, Message, UseCardMsg

if TYPE_CHECKING:
    from gisim.game import GameInfo


class Card(BaseModel):
    id: int
    name: str
    costs: dict[ElementType, int]
    text: str
    card_type: CardType

    def use_card(
        self,
        msg_queue: PriorityQueue[Message],
        game_info: "GameInfo",
    ):
        pass


class TalentCard(Card):
    character_name: str
    card_type: CardType = CardType.TALENT


class WeaponCard(Card):
    weapon_type: WeaponType
    card_type: CardType = CardType.WEAPON

    def use_card(self, msg_queue: PriorityQueue[Message], game_info: "GameInfo"):
        top_msg = msg_queue.queue[0]
        top_msg = cast(UseCardMsg, top_msg)
        player_id, entity_type, idx = top_msg.card_target[0]
        char_pos = CharPos(idx)
        new_msg = GenerateEquipmentMsg(
            sender_id=player_id,
            target=(player_id, char_pos),
            equipment_name=self.name,
            equipment_type=EquipmentType.WEAPON,
        )
        msg_queue.put(new_msg)
        

from queue import PriorityQueue
from typing import TYPE_CHECKING, Dict, cast

from pydantic import BaseModel

from gisim.classes.enums import (
    CardType,
    CharPos,
    ElementType,
    EntityType,
    EquipmentType,
    EventType,
    PlayerID,
    WeaponType,
)
from gisim.classes.message import GenerateEquipmentMsg, Message, UseCardMsg

if TYPE_CHECKING:
    from gisim.game import GameInfo


class Card(BaseModel):
    """
    卡牌基类
    ~~~~~~~
    """

    id: int
    name: str
    costs: Dict[ElementType, int]
    text: str
    card_type: CardType
    combat_action: bool = False
    """Whether this card contains a combat action. e.g. most of the talents & Plunging Strike"""

    def use_card(
        self,
        msg_queue: PriorityQueue,  # PriorityQueue[Message]
        game_info: "GameInfo",
    ):
        pass


class TalentCard(Card):
    character_name: str
    card_type: CardType = CardType.EQUIPMENT
    equipment_type: EquipmentType = EquipmentType.TALENT


class WeaponCard(Card):
    weapon_type: WeaponType
    card_type: CardType = CardType.EQUIPMENT
    equipment_type: EquipmentType = EquipmentType.WEAPON

    def use_card(self, msg_queue: PriorityQueue, game_info: "GameInfo"):
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


class EventCard(Card):
    card_type: CardType = CardType.EVENT
    event_type: EventType = EventType.NORMAL


class FoodCard(EventCard):
    event_type: EventType = EventType.FOOD

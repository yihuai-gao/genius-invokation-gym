from queue import PriorityQueue
from typing import TYPE_CHECKING

from pydantic import BaseModel

from gisim.classes.enums import CardType, CharPos, ElementType, EntityType, PlayerID
from gisim.classes.message import Message

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
        card_user_pos: tuple[PlayerID, CharPos],
        card_target: list[tuple[PlayerID, EntityType, int]] = [],
    ):
        pass


class TalentCard(Card):
    character_name: str
    card_type: CardType = CardType.TALENT

from queue import PriorityQueue

from pydantic import BaseModel

from gisim.classes.enums import CardType, ElementType
from gisim.classes.message import Message


class Card(BaseModel):
    id: int
    name: str
    costs: list[tuple[ElementType, int]]
    text: str
    card_type: CardType

    def use_card(self, msg_queue: PriorityQueue[Message]):
        pass


class TalentCard(Card):
    character_name: str
    card_type: CardType = CardType.TALENT

"""Player area of the Genius Invokation
Note that player agents does not directly talk to this area, but through the judger who judges the validity of each move. The judger then publish events and then the entities in the each player area respond to it in a specific order.
"""

from collections import OrderedDict
from random import Random
from typing import TYPE_CHECKING

from gisim.cards.characters import CHARACTER_CARDS, CHARACTER_NAME2ID, CHARACTER_SKILLS
from gisim.classes.character import CharacterEntity
from gisim.classes.enums import *

if TYPE_CHECKING:
    from gisim.classes.status import CombatStatusEntity
    from gisim.classes.summon import Summon
    from gisim.classes.support import Support
    from gisim.game import Game


class PlayerArea:
    def __init__(
        self,
        parent: "Game",
        random_state: "Random",
        player_id: "PlayerID",
        deck: dict,
    ):
        self.deck = Deck(self, random_state, deck["cards"])
        self.deck.shuffle()
        self._random_state = random_state
        self._parent = parent
        self.player_id = player_id
        self.hand = Hand(self)
        self.element_zone = DiceZone(self, random_state)
        self.character_zone = CharacterZone(self, deck["characters"])
        self.summon_zone = SummonZone(self)
        self.support_zone = SupportZone(self)
        self.combat_status_zone = CombatStatusZone(self)
        """For team combat status only. The status entities of the single character belong to the `CharacterStatus` of the `CharacterZone`"""

    def encode(self, viewer_id: PlayerID):
        return OrderedDict(
            {
                "player_id": self.player_id,
                "deck": self.deck.encode(viewer_id),
                "hand": self.hand.encode(viewer_id),
                "element_zone": self.element_zone.encode(viewer_id),
                "character_zone": self.character_zone.encode(),
                "summon_zone": self.summon_zone.encode(),
                "support_zone": self.support_zone.encode(),
                "combat_status_zone": self.combat_status_zone.encode(),
                "active_character_position": self.character_zone.get_active_character_position()
            }
        )


class Hand:
    def __init__(self, parent: "PlayerArea"):
        self._parent = parent
        self.cards: list[str] = []

    def encode(self, viewer_id):
        return {
            "length": len(self.cards),
            "items": self.cards
            if viewer_id == self._parent.player_id or viewer_id == 0
            else None,
        }


class CharacterZone:
    def __init__(self, parent: "PlayerArea", characters: list[str]):
        self._parent = parent
        assert len(characters) == 3, "Number of characters should be 3"
        self.characters: list["CharacterEntity"] = [
            CharacterEntity(name, self._parent.player_id, CharacterPosition(i))
            for i, name in enumerate(characters)
        ]

    def encode(self):
        return [self.characters[k].encode() for k in range(3)]
    
    def get_active_character_position(self):
        for k in range(3):
            chr = self.characters[k]
            if chr.active:
                return chr.position
        return CharacterPosition.NONE


class SummonZone:
    def __init__(self, parent: "PlayerArea"):
        self._parent = parent
        self.summons: list["Summon"] = []

    def encode(self):
        return [summon.encode() for summon in self.summons]


class SupportZone:
    def __init__(self, parent: "PlayerArea"):
        self._parent = parent
        self.supports: list["Support"] = []

    def encode(self):
        return [support.encode() for support in self.supports]


class DiceZone:
    def __init__(self, parent: "PlayerArea", random_state: Random):
        self._parent = parent
        self._random_state = random_state
        self.dice: list[ElementType] = []

    def roll_dice(self, dice_num=8):
        self.dice = [ElementType(self._random_state.choice(8)) for _ in range(dice_num)]

    def encode(self, viewer_id):
        return {
            "length": len(self.dice),
            "items": self.dice
            if viewer_id == self._parent.player_id or viewer_id == 0
            else None,
        }


class Deck:
    def __init__(self, parent: "PlayerArea", random_state: Random, cards: list[str]):
        self._parent = parent
        self._random_state = random_state
        self.original_cards = cards
        self.cards = cards

    def shuffle(self):
        self._random_state.shuffle(self.cards)

    def draw_cards(self, n):
        assert n <= len(self.cards), "Card number to be drawn exceeds the deck size"
        output = self.cards[:n]
        self.cards = self.cards[n:]
        return output

    def encode(self, viewer_id):
        return {
            "length": len(self.cards),
            "items": [card for card in self.original_cards if card in self.cards]
            if viewer_id == self._parent.player_id or viewer_id == 0
            else None,
        }


class CombatStatusZone:
    def __init__(self, parent: "PlayerArea"):
        self._parent = parent
        self.status_entities: list["CombatStatusEntity"] = []

    def encode(self):
        return [status_entity.encode() for status_entity in self.status_entities]

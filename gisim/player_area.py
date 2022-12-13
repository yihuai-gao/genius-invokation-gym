"""Player area of the Genius Invokation
Note that player agents does not directly talk to this area, but through the game who judges the validity of each move. The judger then publish events and then the entities in the each player area respond to it in a specific order.
"""

from collections import OrderedDict
from multiprocessing.sharedctypes import Value
from random import Random
from typing import TYPE_CHECKING, Optional

from classes.card import CardEntity

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
        self.declare_end = False
        "Whether a player has declared end of the round"
        self.deck = Deck(self, random_state, deck["cards"])
        self.deck.shuffle()
        self._random_state = random_state
        self._parent = parent
        self.player_id = player_id
        self.hand = Hand(self)
        self.dice_zone = DiceZone(self, random_state)
        self.character_zone = CharacterZone(self, deck["characters"])
        self.summon_zone = SummonZone(self)
        self.support_zone = SupportZone(self)
        self.combat_status_zone = CombatStatusZone(self)
        """For team combat status only. The status entities of the single character belong to the `CharacterStatus` of the `CharacterZone`"""

    def encode(self, viewer_id: PlayerID):
        return OrderedDict(
            {
                "player_id": self.player_id,
                "declared_end": self.declare_end,
                "deck": self.deck.encode(viewer_id),
                "hand": self.hand.encode(viewer_id),
                "dice_zone": self.dice_zone.encode(viewer_id),
                "character_zone": self.character_zone.encode(),
                "summon_zone": self.summon_zone.encode(),
                "support_zone": self.support_zone.encode(),
                "combat_status_zone": self.combat_status_zone.encode(),
                "active_character_position": self.character_zone.get_active_character_position(),
            }
        )


class Hand:
    def __init__(self, parent: "PlayerArea"):
        self._parent = parent
        self.cards: list[CardEntity] = []

    @property
    def card_names(self):
        return [card.name for card in self.cards]

    def add_cards(self, card_names: list[str]):
        for name in card_names:
            self.cards.append(CardEntity(name))

    def remove_cards(self, cards_idx: list[int]):
        removed_names: list[str] = []
        for i in sorted(cards_idx, reverse=True):
            removed_names.append(self.cards[i].name)
            del self.cards[i]
        return removed_names

    def encode(self, viewer_id):
        return {
            "length": len(self.cards),
            "items": self.card_names
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

    @property
    def active_character(self):
        return self.characters[self.get_active_character_position().value]


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
        self._dice: list[ElementType] = []
        self.init_dice_num = 8
        self.fixed_dice: list[ElementType] = []
        self.max_reroll_round = 1

    def init_dice(self):
        self._dice = []
        self.add_dice(self.init_dice_num)
        self.remaining_reroll_round = self.max_reroll_round
        # TODO: fixed dice from artifact/support

    def reroll_dice(self, dice_idx: list[int]):
        self.remove_dice(dice_idx)
        self.add_dice(dice_num=len(dice_idx))
        self.remaining_reroll_round -= 1
        return self.remaining_reroll_round

    def add_dice(self, dice_num, element_type: Optional[ElementType] = None):
        if element_type == None:
            self._dice += [
                ElementType(self._random_state.choice([range(8)]))
                for _ in range(dice_num)
            ]
        else:
            self._dice += [element_type for _ in range(dice_num)]

    def remove_dice(self, dice_idx: list[int]):
        for i in sorted(dice_idx, reverse=True):
            del self._dice[i]

    def encode(self, viewer_id):
        return {
            "length": len(self._dice),
            "items": self._dice
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

    def draw_cards(self, n: int):
        assert n <= len(self.cards), "Card number to be drawn exceeds the deck size"
        output = self.cards[:n]
        self.cards = self.cards[n:]
        return output

    def encode(self, viewer_id: PlayerID):
        return {
            "length": len(self.cards),
            "items": [card for card in self.original_cards if card in self.cards]
            if viewer_id == self._parent.player_id or viewer_id == 0
            else None,
        }

    def add_cards(self, card_names: list[str]):
        self.cards += card_names


class CombatStatusZone:
    def __init__(self, parent: "PlayerArea"):
        self._parent = parent
        self.status_entities: list["CombatStatusEntity"] = []

    def encode(self):
        return [status_entity.encode() for status_entity in self.status_entities]

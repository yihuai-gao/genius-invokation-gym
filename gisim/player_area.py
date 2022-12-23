"""Player area of the Genius Invokation
Note that player agents does not directly talk to this area, but through the game who judges the validity of each move. The judger then publish events and then the entities in the each player area respond to it in a specific order.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from multiprocessing.sharedctypes import Value
from queue import PriorityQueue
from random import Random
from typing import TYPE_CHECKING, Generic, Optional, TypeVar, cast
from xml.dom.minidom import Element

from gisim.cards.characters import CHARACTER_CARDS, CHARACTER_NAME2ID, CHARACTER_SKILLS
from gisim.cards.equipments import talents
from gisim.classes.action import RollDiceAction
from gisim.classes.character import CharacterEntity, CharacterEntityInfo
from gisim.classes.entity import (
    ArtifactEntity,
    CardEntity,
    Entity,
    StatusEntity,
    TalentEntity,
    WeaponEntity,
)
from gisim.classes.enums import *
from gisim.classes.message import ChangeDiceMsg, Message, PayCardCostMsg, PayCostMsg

if TYPE_CHECKING:
    from gisim.classes.status import CombatStatusEntity
    from gisim.classes.summon import Summon
    from gisim.classes.support import Support
    from gisim.game import Game


class BaseZone(Entity, ABC):
    @abstractmethod
    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        ...


class PlayerArea(BaseZone):
    def __init__(
        self,
        parent: "Game",
        random_state: "Random",
        player_id: "PlayerID",
        deck: dict,
    ):
        super().__init__()
        self.declare_end = False
        "Whether a player has declared end of the round"
        self._random_state = random_state
        self._parent = parent
        self.player_id = player_id
        self.card_zone = CardZone(self, random_state, deck["cards"])
        self.card_zone.shuffle()
        self.dice_zone = DiceZone(self, random_state)
        self.character_zones: list["CharacterZone"] = [
            CharacterZone(self, name, CharPos(i))
            for i, name in enumerate(deck["characters"])
        ]
        self.summon_zone = SummonZone(self)
        self.support_zone = SupportZone(self)
        self.combat_status_zone = CombatStatusZone(self)
        """For team combat status only. The status entities of the single character belong to the `CharacterStatus` of the `CharacterZone`"""

    @property
    def active_character(self):
        if self.get_active_character_position().value is None:
            return None
        return self.character_zones[self.get_active_character_position().value]

    @property
    def background_characters(self):
        active_pos_val = self.get_active_character_position().value
        return [
            self.character_zones[(active_pos_val + 1) % 3],
            self.character_zones[(active_pos_val + 2) % 3],
        ]

    def get_active_character_position(self):
        for k in range(3):
            chr = self.character_zones[k]
            if chr.character.active:
                return chr.position
        return CharPos.NONE

    def encode(self, viewer_id: PlayerID):
        return OrderedDict(
            {
                "player_id": self.player_id,
                "declared_end": self.declare_end,
                "card_zone": self.card_zone.encode(viewer_id),
                "dice_zone": self.dice_zone.encode(viewer_id),
                "character_zones": [self.character_zones[k].encode() for k in range(3)],
                "summon_zone": self.summon_zone.encode(),
                "support_zone": self.support_zone.encode(),
                "combat_status_zone": self.combat_status_zone.encode(),
                "active_character_position": self.get_active_character_position(),
            }
        )

    def get_zones(self, zone_type: RegionType) -> list[BaseZone]:
        assert isinstance(zone_type, RegionType), "zone_type should be RegionType"

        if zone_type == RegionType.CHARACTER_ACTIVE:
            active_pos_val = self.get_active_character_position().value
            zones = [self.active_character]

        elif zone_type == RegionType.CHARACTER_BACKGROUND:
            zones = self.background_characters

        elif zone_type == RegionType.CHARACTER_LEFT:
            zones = [self.character_zones[0]]

        elif zone_type == RegionType.CHARACTER_MIDDLE:
            zones = [self.character_zones[1]]

        elif zone_type == RegionType.CHARACTER_RIGHT:
            zones = [self.character_zones[2]]

        elif zone_type == RegionType.CHARACTER_ALL:
            zones = self.character_zones

        elif zone_type == RegionType.SUPPORT_ZONE:
            zones = [self.support_zone]

        elif zone_type == RegionType.SUMMON_ZONE:
            zones = [self.summon_zone]

        elif zone_type == RegionType.CARD_ZONE:
            zones = [self.card_zone]

        elif zone_type == RegionType.COMBAT_STATUS_ZONE:
            zones = [self.combat_status_zone]

        elif zone_type == RegionType.DICE_ZONE:
            zones = [self.dice_zone]

        elif zone_type == RegionType.ALL:
            zones = [
                self.card_zone,
                self.active_character,
                self.combat_status_zone,
                *self.background_characters,
                self.summon_zone,
                self.support_zone,
                self.dice_zone,
            ]

        else:
            raise ValueError("Current `zone_type` is not in the player area.")

        return cast(list[BaseZone], zones)

    def msg_handler(self, msg_queue: PriorityQueue[Message]) -> bool:
        ...


class CardZone(BaseZone):
    def __init__(self, parent: "PlayerArea", random_state: Random, cards: list[str]):
        super().__init__()
        self._parent = parent
        self._random_state = random_state
        self.deck_original_cards = cards
        self.deck_cards = cards
        self.hand_cards: list[CardEntity] = []

    def shuffle(self):
        self._random_state.shuffle(self.deck_cards)

    @property
    def card_names(self):
        return [card.name for card in self.hand_cards]

    def draw_cards_from_deck(self, n: int):
        assert n <= len(
            self.deck_cards
        ), "Card number to be drawn exceeds the deck size"
        drawn_cards = self.deck_cards[:n]
        self.deck_cards = self.deck_cards[n:]
        for card_name in drawn_cards:
            self.hand_cards.append(CardEntity(card_name))

    def remove_hand_cards(self, cards_idx: list[int]):
        removed_names: list[str] = []
        for i in sorted(cards_idx, reverse=True):
            removed_names.append(self.hand_cards[i].name)
            del self.hand_cards[i]
        return removed_names

    def encode(self, viewer_id):
        show_names = viewer_id in [self._parent.player_id, PlayerID.SPECTATOR]
        return OrderedDict(
            {
                "deck_length": len(self.deck_cards),
                "hand_length": len(self.hand_cards),
                "deck_cards": self.deck_cards if show_names else None,
                "hand_cards": [card.name for card in self.hand_cards]
                if show_names
                else None,
            }
        )

    def msg_handler(self, msg_queue: PriorityQueue[Message]) -> bool:
        ...


class SummonZone(BaseZone):
    def __init__(self, parent: "PlayerArea"):
        super().__init__()
        self._parent = parent
        self.summons: list["Summon"] = []

    def encode(self):
        return [summon.encode() for summon in self.summons]

    def msg_handler(self, msg_queue: PriorityQueue[Message]) -> bool:
        ...


class SupportZone(BaseZone):
    def __init__(self, parent: "PlayerArea"):
        super().__init__()
        self._parent = parent
        self.supports: list["Support"] = []

    def encode(self):
        return [support.encode() for support in self.supports]

    def msg_handler(self, msg_queue: PriorityQueue[Message]) -> bool:
        ...


class DiceZone(BaseZone):
    def __init__(self, parent: "PlayerArea", random_state: Random):
        super().__init__()
        self._parent = parent
        self._random_state = random_state
        self._dice: list[ElementType] = []
        self.init_dice_num = 8
        self.fixed_dice: list[ElementType] = []
        self.max_reroll_chance = 1

    def init_dice(self):
        self._dice = []
        self.add_dice([ElementType.ANY] * self.init_dice_num)
        self.remaining_reroll_chance = self.max_reroll_chance
        # TODO: fixed dice from artifact/support

    def reroll_dice(self, dice_idx: list[int]):
        self.remove_dice(dice_idx)
        self.add_dice([ElementType.ANY for _ in dice_idx])
        self.remaining_reroll_chance -= 1
        return self.remaining_reroll_chance

    def add_dice(self, element_types: list[ElementType]):
        for element_type in element_types:
            if element_type == ElementType.ANY:
                self._dice.append(
                    ElementType(self._random_state.choice(list(range(8))))
                )
            elif element_type == ElementType.BASIC:
                self._dice.append(
                    ElementType(self._random_state.choice(list(range(1, 8))))
                )
            else:
                self._dice.append(element_type)

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

    def msg_handler(self, msg_queue: PriorityQueue[Message]) -> bool:
        msg = msg_queue.queue[0]
        if self._uuid in msg.responded_entities:
            return False
        if isinstance(msg, ChangeDiceMsg):
            msg = cast(ChangeDiceMsg, msg)
            self.remove_dice(msg.remove_dice_idx)
            self.add_dice(msg.new_target_element)
            if msg.update_max_reroll_chance is not None:
                self.max_reroll_chance = msg.update_max_reroll_chance
            if msg.consume_reroll_chance:
                self.remaining_reroll_chance -= 1
            msg.responded_entities.append(self._uuid)
            return True
        if isinstance(msg, PayCostMsg):
            msg = cast(PayCostMsg, msg)
            self.remove_dice(msg.paid_dice_idx)
            msg.responded_entities.append(self._uuid)
            return True

        return False


class CombatStatusZone(BaseZone):
    def __init__(self, parent: "PlayerArea"):
        super().__init__()
        self._parent = parent
        self.status_entities: list["CombatStatusEntity"] = []

    def encode(self):
        return [status_entity.encode() for status_entity in self.status_entities]

    def msg_handler(self, msg_queue: PriorityQueue[Message]) -> bool:
        ...


class CharacterZone(BaseZone):
    """Including entity, talent, weapon, artifact, status"""

    def __init__(self, parent: "PlayerArea", name: str, char_pos: CharPos):
        super().__init__()
        self._parent = parent
        self.position: CharPos = char_pos
        self.character = CharacterEntity(name, self._parent.player_id, char_pos)
        self.talent: Optional[TalentEntity] = None
        self.weapon: Optional[WeaponEntity] = None
        self.artifact: Optional[ArtifactEntity] = None
        self.status: list[StatusEntity] = []

    def encode(self):
        return {
            "character": self.character.encode(),
            "talent": self.talent.encode() if self.talent else None,
            "weapon": self.weapon.encode() if self.weapon else None,
            "artifact": self.artifact.encode() if self.artifact else None,
            "status": [status.encode() for status in self.status],
        }

    def msg_handler(self, msg_queue: PriorityQueue[Message]) -> bool:
        updated = False
        entities = [
            self.character,
            self.talent,
            self.weapon,
            self.artifact,
            *self.status,
        ]
        entities = cast(list[Entity], entities)
        for entity in entities:
            if entity is None:
                continue
            updated = entity.msg_handler(msg_queue)
            if updated:
                return True
        return False


class PlayerInfo:
    def __init__(self, player_info_dict: OrderedDict):
        self.player_info_dict = player_info_dict
        self.player_id: PlayerID = player_info_dict["player_id"]
        self.declared_end: bool = player_info_dict["declared_end"]
        self.hand_length: int = player_info_dict["card_zone"]["hand_length"]
        self.hand_cards: list = player_info_dict["card_zone"]["hand_cards"]
        self.deck_length: int = player_info_dict["card_zone"]["deck_length"]
        self.deck: list[str] = player_info_dict["card_zone"]["deck_cards"]
        self.dice_zone_len: int = player_info_dict["dice_zone"]["length"]
        self.dice_zone: list[ElementType] = player_info_dict["dice_zone"]["items"]
        self.summon_zone: list[Summon] = player_info_dict["summon_zone"]
        self.support_zone: list[Support] = player_info_dict["support_zone"]
        self.combat_status_zone: list[CombatStatusEntity] = player_info_dict[
            "combat_status_zone"
        ]
        self.characters: list[CharacterInfo] = [
            CharacterInfo(player_info_dict["character_zones"][k]) for k in range(3)
        ]
        self.active_character_position: CharPos = player_info_dict[
            "active_character_position"
        ]


class CharacterInfo:
    def __init__(self, character_info_dict: OrderedDict):
        self.character = CharacterEntityInfo(character_info_dict["character"])
        self.talent = character_info_dict["talent"]
        self.weapon = character_info_dict["weapon"]
        self.artifact = character_info_dict["artifact"]
        self.status = character_info_dict["status"]

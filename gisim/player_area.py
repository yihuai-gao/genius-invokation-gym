"""Player area of the Genius Invokation
Note that player agents does not directly talk to this area, but through the game who judges the validity of each move. The judger then publish events and then the entities in the each player area respond to it in a specific order.
"""

from abc import ABC, abstractmethod
from collections import OrderedDict
from logging import getLogger
from queue import PriorityQueue
from random import Random
from typing import TYPE_CHECKING, Generic, List, Optional, TypeVar, cast
from uuid import uuid4

from gisim.cards import get_card, get_equipment, get_summon_entity
from gisim.cards.base import Card
from gisim.classes.character import CharacterEntity, CharacterEntityInfo
from gisim.classes.entity import Entity
from gisim.classes.enums import *
from gisim.classes.equipment import ArtifactEntity, TalentEntity, WeaponEntity
from gisim.classes.message import (
    AfterUsingSkillMsg,
    ChangeCardsMsg,
    ChangeDiceMsg,
    DealDamageMsg,
    ElementalReactionTriggeredMsg,
    GenerateCharacterStatusMsg,
    GenerateCombatStatusMsg,
    GenerateEquipmentMsg,
    GenerateSummonMsg,
    Message,
    PayCardCostMsg,
    PayCostMsg,
    RoundBeginMsg,
    RoundEndMsg,
    TriggerSummonEffectMsg,
    UseCardMsg,
)

# from gisim.classes.status import CharacterStatusEntity, get_character_status_entity
from gisim.status import (
    CharacterStatusEntity,
    CombatStatusEntity,
    get_character_status_entity,
    get_combat_status_entity,
)

if TYPE_CHECKING:
    from gisim.classes.status import CombatStatusEntity
    from gisim.classes.summon import Summon
    from gisim.classes.support import Support
    from gisim.game import Game


class BaseZone(ABC):
    def __init__(self):
        self._uuid = uuid4()
        self._logger = getLogger("gisim")

    @abstractmethod
    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        ...


class PlayerArea(BaseZone):
    declare_end: bool

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
        self.character_zones: List["CharacterZone"] = [
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
        if active_pos_val := self.get_active_character_position().value:
            return [
                self.character_zones[(active_pos_val + 1) % 3],
                self.character_zones[(active_pos_val + 2) % 3],
            ]
        else:
            return self.character_zones

    def get_active_character_position(self):
        for k in range(3):
            chr = self.character_zones[k]
            if chr.character.active:
                return chr.position
        return CharPos.NONE

    def get_game_info(self):
        return self._parent.encode_game_info(viewer_id=self.player_id)

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

    def get_zones(self, zone_type: RegionType) -> List[BaseZone]:
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

        return cast(List[BaseZone], zones)

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        ...


class CardZone(BaseZone):
    def __init__(self, parent: "PlayerArea", random_state: Random, cards: List[str]):
        super().__init__()
        self._parent = parent
        self._random_state = random_state
        self.deck_original_cards = cards
        self.deck_cards = cards
        self.hand_cards: List[Card] = []

    def shuffle(self):
        self._random_state.shuffle(self.deck_cards)

    @property
    def card_names(self):
        return [card.name for card in self.hand_cards]

    def draw_cards_from_deck(self, cards_type: List[CardType]):
        drawn_cards = []
        for card_type in cards_type:
            if len(self.deck_cards) == 0:
                break
            if card_type == CardType.ANY:
                drawn_cards.append(self.deck_cards[0])
                self.deck_cards.pop(0)
            else:
                for idx, card_name in enumerate(self.deck_cards[0]):
                    deck_card_type = get_card(card_name).card_type
                    if card_type == deck_card_type:
                        drawn_cards.append(self.deck_cards[idx])
                        self.deck_cards.pop(idx)
                        break

        for card_name in drawn_cards:
            self.hand_cards.append(get_card(card_name))

    def remove_hand_cards(self, cards_idx: List[int]):
        removed_names: List[str] = []
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

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        if top_msg.sender_id == ~self._parent.player_id:
            return False
        updated = False
        if isinstance(top_msg, PayCardCostMsg):
            top_msg = cast(PayCardCostMsg, top_msg)
            card = self.hand_cards[top_msg.card_idx]
            top_msg.required_cost = card.costs
            updated = True

        if isinstance(top_msg, UseCardMsg):
            top_msg = cast(UseCardMsg, top_msg)
            card = self.hand_cards[top_msg.card_idx]
            card.use_card(
                msg_queue,
                self._parent.get_game_info(),
            )
            del self.hand_cards[top_msg.card_idx]
            updated = True

        if isinstance(top_msg, ChangeCardsMsg):
            top_msg = cast(ChangeCardsMsg, top_msg)
            self.remove_hand_cards(top_msg.discard_cards_idx)
            self.draw_cards_from_deck(top_msg.draw_cards_type)
            updated = True

        if isinstance(top_msg, RoundEndMsg):
            self.draw_cards_from_deck([CardType.ANY, CardType.ANY])
            updated = True

        if updated:
            top_msg.responded_entities.append(self._uuid)

        return updated


class SummonZone(BaseZone):
    def __init__(self, parent: "PlayerArea"):
        super().__init__()
        self._parent = parent
        self.summons: List["Summon"] = []
        self.summon_limit: int = 4
        """4 Summons at most in each player's summon zone"""

    def encode(self):
        return [summon.encode() for summon in self.summons]

    def remove_summon(self, idx: int):
        target_summon = self.summons[idx]
        target_summon.active = False
        target_summon.position = -1
        self.summons.pop(idx)
        for idx, summon in enumerate(self.summons):
            # Reset positions
            summon.position = idx

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        msg = msg_queue.queue[0]
        if self._uuid in msg.responded_entities:
            return False
        updated = False
        if isinstance(msg, GenerateSummonMsg):
            msg = cast(GenerateSummonMsg, msg)
            if msg.target_id == self._parent.player_id:
                if len(self.summons) == self.summon_limit:
                    """Remove the first summon in the zone"""
                    self.remove_summon(0)

                new_summon = get_summon_entity(msg.summon_name, msg.target_id)
                new_summon.position = len(self.summons)
                self.summons.append(new_summon)
                updated = True
                msg.responded_entities.append(self._uuid)

        # 请求触发召唤物效果
        if isinstance(msg, TriggerSummonEffectMsg):
            for summon in self.summons:
                if summon.name in msg.summon_list:
                    updated = summon.msg_handler(msg_queue)
                msg.responded_entities.append(self._uuid)

        # 触发元素反应
        if isinstance(msg, ElementalReactionTriggeredMsg):
            for summon in self.summons:
                updated = summon.msg_handler(msg_queue)
                msg.responded_entities.append(self._uuid)

        if isinstance(msg, RoundEndMsg):
            for idx, summon in enumerate(self.summons):
                updated = summon.msg_handler(msg_queue)
                if updated:
                    if not summon.active:
                        # Running out of usage: will be removed
                        self.remove_summon(idx)
                    return True
            # None of the summons responded:
            msg.responded_entities.append(self._uuid)
            return False

        return updated


class SupportZone(BaseZone):
    def __init__(self, parent: "PlayerArea"):
        super().__init__()
        self._parent = parent
        self.supports: List["Support"] = []

    def encode(self):
        return [support.encode() for support in self.supports]

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        ...


class DiceZone(BaseZone):
    def __init__(self, parent: "PlayerArea", random_state: Random):
        super().__init__()
        self._parent = parent
        self._random_state = random_state
        self._dice: List[ElementType] = []
        self.init_dice_num = 8
        self.fixed_dice: List[ElementType] = []
        self.max_reroll_chance = 1

    def init_dice(self):
        self._dice = []
        self.add_dice([ElementType.ANY] * self.init_dice_num)
        self.remaining_reroll_chance = self.max_reroll_chance
        # TODO: fixed dice from artifact/support

    def reroll_dice(self, dice_idx: List[int]):
        self.remove_dice(dice_idx)
        self.add_dice([ElementType.ANY for _ in dice_idx])
        self.remaining_reroll_chance -= 1
        return self.remaining_reroll_chance

    def add_dice(self, element_types: List[ElementType]):
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

    def remove_dice(self, dice_idx: List[int]):
        for i in sorted(dice_idx, reverse=True):
            del self._dice[i]

    def encode(self, viewer_id):
        return {
            "length": len(self._dice),
            "items": self._dice if viewer_id in [self._parent.player_id, 0] else None,
        }

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        msg = msg_queue.queue[0]
        if self._uuid in msg.responded_entities:
            return False
        updated = False
        if isinstance(msg, ChangeDiceMsg):
            if self._parent.player_id != msg.sender_id:
                return False
            msg = cast(ChangeDiceMsg, msg)
            self.remove_dice(msg.remove_dice_idx)
            self.add_dice(msg.new_target_element)
            if msg.update_max_reroll_chance is not None:
                self.max_reroll_chance = msg.update_max_reroll_chance
            if msg.consume_reroll_chance:
                self.remaining_reroll_chance -= 1
            updated = True
        elif isinstance(msg, PayCostMsg):
            if self._parent.player_id != msg.sender_id:
                return False
            msg = cast(PayCostMsg, msg)
            if not msg.simulate:
                self.remove_dice(msg.paid_dice_idx)
            updated = True

        if updated:
            msg.responded_entities.append(self._uuid)

        return updated


class CombatStatusZone(BaseZone):
    def __init__(self, parent: "PlayerArea"):
        super().__init__()
        self._parent = parent
        self.status_entities: List["CombatStatusEntity"] = []

    def encode(self):
        return [status_entity.encode() for status_entity in self.status_entities]

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        top_msg = msg_queue.queue[0]

        if isinstance(top_msg, GenerateCombatStatusMsg):
            # 创建出战阵营状态
            top_msg = cast(GenerateCombatStatusMsg, top_msg)
            if top_msg.target_player_id == self._parent.player_id:
                for idx, entity in enumerate(self.status_entities):
                    if entity.name == top_msg.combat_status_name:
                        self.status_entities.pop(idx)
                status_entity = get_combat_status_entity(
                    top_msg.combat_status_name,
                    self._parent.player_id,
                    top_msg.remaining_round,
                    top_msg.remaining_usage,
                )
                self.status_entities.append(status_entity)
                top_msg.responded_entities.append((self._uuid))

        for entity in self.status_entities:
            if updated := entity.msg_handler(msg_queue):
                return True

        # 删除用完或者到回合次数的出战阵营状态
        if isinstance(top_msg, RoundEndMsg):
            invalid_idxes = [
                idx
                for idx, status in enumerate(self.status_entities)
                if (status.remaining_round == 0 or status.remaining_usage == 0)
                and status.active == False
            ]
            invalid_idxes.reverse()
            for idx in invalid_idxes:
                self.status_entities.pop(idx)
        return False


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
        self.status: List[CharacterStatusEntity] = []

    def encode(self):
        return {
            "character": self.character.encode(),
            "talent": self.talent.encode() if self.talent else None,
            "weapon": self.weapon.encode() if self.weapon else None,
            "artifact": self.artifact.encode() if self.artifact else None,
            "status": [status.encode() for status in self.status],
        }

    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        if not self.character.alive and not self.character.active:
            # Return immediately if the character has already died.
            return False

        updated = False
        top_msg = msg_queue.queue[0]

        # Generate entities for this character
        # Will be ignored if character zone has already executed this message

        if self._uuid not in top_msg.responded_entities:
            if isinstance(top_msg, GenerateCharacterStatusMsg):
                top_msg = cast(GenerateCharacterStatusMsg, top_msg)
                if top_msg.target == (self._parent.player_id, self.position):
                    for idx, entity in enumerate(self.status):
                        if entity.name == top_msg.status_name:
                            self.status.pop(idx)

                    status_entity = get_character_status_entity(
                        top_msg.status_name,
                        self._parent.player_id,
                        self.position,
                        top_msg.status_type,
                        top_msg.remaining_round,
                        top_msg.remaining_usage,
                    )
                    self.status.append(status_entity)
                    top_msg.responded_entities.append((self._uuid))

            elif isinstance(top_msg, GenerateEquipmentMsg):
                top_msg = cast(GenerateEquipmentMsg, top_msg)
                if top_msg.target == (self._parent.player_id, self.position):
                    equipment_entity = get_equipment(
                        top_msg.equipment_name, top_msg.target
                    )
                    if top_msg.equipment_type == EquipmentType.WEAPON:
                        equipment_entity = cast(WeaponEntity, equipment_entity)
                        self.weapon = equipment_entity
                    elif top_msg.equipment_type == EquipmentType.ARTIFACT:
                        equipment_entity = cast(ArtifactEntity, equipment_entity)
                        self.artifact = equipment_entity
                    elif top_msg.equipment_type == EquipmentType.TALENT:
                        equipment_entity = cast(TalentEntity, equipment_entity)
                        self.talent = equipment_entity
                    else:
                        raise ValueError("Wrong equipment type!")
                    top_msg.responded_entities.append((self._uuid))

        atk_buff = []
        def_buff = []
        under_atk_buff = []
        neg_buff = []

        for buff in self.status:
            if buff.status_type == StatusType.ATTACK_BUFF:
                atk_buff.append(buff)
            elif buff.status_type == StatusType.DEFENSE_BUFF:
                def_buff.append(buff)
            elif buff.status_type == StatusType.UNDER_ATTACK_BUFF:
                under_atk_buff.append(buff)
            elif buff.status_type == StatusType.NEGATIVE_BUFF:
                neg_buff.append(buff)

        entities = [
            *under_atk_buff,
            *def_buff,
            self.character,
            self.talent,
            self.weapon,
            self.artifact,
            *atk_buff,
            *neg_buff,
        ]
        entities = cast(List[Entity], entities)
        for entity in entities:
            if entity is None:
                continue
            if updated := entity.msg_handler(msg_queue):
                return True

        # Remove
        if isinstance(top_msg, RoundEndMsg):
            invalid_idxes = [
                idx
                for idx, status in enumerate(self.status)
                if (status.remaining_round == 0 or status.remaining_usage == 0)
                and status.active == False
            ]
            invalid_idxes.reverse()
            for idx in invalid_idxes:
                self.status.pop(idx)
        return False


class PlayerInfo:
    def __init__(self, player_info_dict: OrderedDict):
        self.player_info_dict = player_info_dict
        self.player_id: PlayerID = player_info_dict["player_id"]
        self.declared_end: bool = player_info_dict["declared_end"]
        self.hand_length: int = player_info_dict["card_zone"]["hand_length"]
        self.hand_cards: List[str] = player_info_dict["card_zone"]["hand_cards"]
        self.deck_length: int = player_info_dict["card_zone"]["deck_length"]
        self.deck: List[str] = player_info_dict["card_zone"]["deck_cards"]
        self.dice_zone_len: int = player_info_dict["dice_zone"]["length"]
        self.dice_zone: List[ElementType] = player_info_dict["dice_zone"]["items"]
        self.summon_zone: List[dict] = player_info_dict["summon_zone"]
        self.support_zone: List[Support] = player_info_dict["support_zone"]
        self.combat_status_zone: List[CombatStatusEntity] = player_info_dict[
            "combat_status_zone"
        ]
        self.characters: List[CharacterInfo] = [
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

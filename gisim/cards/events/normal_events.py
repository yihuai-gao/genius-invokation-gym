from typing import cast

from cards.base import EventCard
from classes.enums import AttackType, CharPos, ElementType
from classes.message import DealDamageMsg, GenerateCharacterStatusMsg, UseCardMsg
from classes.status import CharacterStatusEntity


class HeavyStrikeCard(EventCard):
    # TODO: What is the id of this card?
    id = 10000
    name = "Heavy Strike"
    costs = {ElementType.SAME: 1}
    text = """During this round, your current active character's next Normal Attack deals +1 DMG.
    When this Normal Attack is a Charged Attack: Deal +1 additional DMG."""

    def use_card(self, msg_queue, game_info):
        top_msg = msg_queue.queue[0]
        top_msg = cast(UseCardMsg, top_msg)

        player_id = top_msg.sender_id
        new_msg = GenerateCharacterStatusMsg(
            sender_id=player_id,
            target=(player_id, CharPos.ACTIVE),
            status_name="HeavyStrikeStatus",
        )
        msg_queue.put(new_msg)


class HeavyStrikeStatus(CharacterStatusEntity):
    name: str = "Heavy Strike"
    description: str = """During this round, your current active character's next Normal Attack deals +1 DMG.
    When this Normal Attack is a Charged Attack: Deal +1 additional DMG."""
    value: int = 0  # Useless in this status
    active: bool = True
    remaining_usage: int = 1
    remaining_round: int = 1

    def msg_handler(self, msg_queue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attack_type == AttackType.NORMAL_ATTACK:
                top_msg.targets[0] = (
                    top_msg.targets[0][0],
                    top_msg.targets[0][1],
                    top_msg.targets[0][2],
                    top_msg.targets[0][3] + 1,  # Deal +1 DMG for normal attack
                )
                if top_msg.is_charged_attack:
                    top_msg.targets[0] = (
                        top_msg.targets[0][0],
                        top_msg.targets[0][1],
                        top_msg.targets[0][2],
                        top_msg.targets[0][3]
                        + 1,  # Deal extra +1 DMG for charged attack
                    )
                updated = True
                self.remaining_usage = 0
                self.active = False

        if updated:
            top_msg.responded_entities.append(self._uuid)
        return updated

from abc import ABC, abstractmethod
from collections import OrderedDict
from logging import Logger, getLogger
from queue import PriorityQueue
from typing import cast

from gisim.classes.entity import Entity
from gisim.classes.enums import CharPos, ElementType, PlayerID
from gisim.classes.message import DealDamageMsg, Message, RoundEndMsg
from gisim.env import INF_INT


class CharacterStatusEntity(Entity, ABC):
    """Status which is attached to a fixed character.
    Shown in the upper line of the character card. Will be calculated earlier."""

    player_id: PlayerID
    position: CharPos
    name: str
    description: str
    active: bool
    remaining_round: int
    remaining_usage: int
    value: int

    def msg_handler(self, msg_queue: PriorityQueue):
        ...

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))


class CombatStatusEntity(Entity, ABC):
    """Status which is attached dynamically to the active character.
    Shown in the lower line of the character card. Will be calculated later."""

    player_id: PlayerID
    # position: CharPos = CharPos.ACTIVE
    name: str
    description: str
    active: bool
    remaining_round: int
    value: int

    def encode(self):
        return OrderedDict(self.dict(exclude={"_uuid", "_logger"}))


class ElementalInfusion(CharacterStatusEntity):
    name: str
    element: ElementType
    description: str = "Convert physical damage into elemental damage"
    value: int = 0
    active: bool = True
    remaining_usage: int = INF_INT

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            if top_msg.attacker == (self.player_id, self.position):
                for idx, target in enumerate(top_msg.targets):
                    if target[2] == ElementType.NONE:
                        print(f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {target[2]} -> {target[3]} + Add: 0\n        {self.player_id.name}-{self.position}")
                        top_msg.targets[idx] = (
                            target[0],
                            target[1],
                            self.element,
                            target[3],
                        )
                        updated = True

        if isinstance(top_msg, RoundEndMsg):
            top_msg = cast(RoundEndMsg, top_msg)
            assert (
                self.remaining_round >= 1
            ), "Remaining round should not be lower than 1!"
            self.remaining_round -= 1
            if self.remaining_round == 0:
                self.active = False
        if updated:
            msg_queue.queue[0].responded_entities.append(self._uuid)
        return updated


class FrozenEffect(CharacterStatusEntity):
    """元素反应冻结效果"""
    name: str = "Frozen Effect"
    element: ElementType = ElementType.NONE
    description: str = """[Character Status]the target is unable to perform any Actions this round(Can be removed in advance after the target receives Physical or Pyro DMG, in which case they will take +2 DMG)"""
    value: int = 0
    active: bool = True
    remaining_usage: int = 1

    def msg_handler(self, msg_queue: PriorityQueue):
        top_msg = msg_queue.queue[0]
        if self._uuid in top_msg.responded_entities:
            return False
        updated = False
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            # 负面buff 为别人加伤
            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(top_msg.targets):
                if (target_id, target_pos) == (self.player_id, self.position) and element_type in [ElementType.NONE, ElementType.PYRO]:
                    print(f"    Character Status Effect:\n        {self.name}:{self.description}\n        Origin DMG: {element_type.name} -> {dmg_val} + Add: 2\n        {self.player_id.name}-{self.position} be subjected to Physical or Pyro DMG")
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val + 2,
                    )
                    updated = True
                    # 冻结时遭受物理攻击或者火元素伤害 冻结撤销
                    self.remaining_round = 0
                    self.active = False

        if isinstance(top_msg, RoundEndMsg):
            # 回合结束冻结 撤销
            self.remaining_round = 0
            self.active = False
        if updated:
            msg_queue.queue[0].responded_entities.append(self._uuid)
        return updated


def get_character_status_entity(
    name: str, player_id: PlayerID, position: CharPos, remaining_round: int
):
    stripped_name = name.replace(" ", "")
    if stripped_name.endswith("Infusion"):
        elem_char = stripped_name.replace("Infusion", "").upper()
        element: ElementType = eval(f"ElementType.{elem_char}")
        status = ElementalInfusion(
            name=name,
            player_id=player_id,
            position=position,
            remaining_round=remaining_round,
            element=element,
        )
        status = cast(CharacterStatusEntity, status)
        return status

    status_cls = globals()[stripped_name]
    status: CharacterStatusEntity = status_cls(
        player_id=player_id, position=position, remaining_round=remaining_round
    )
    return status

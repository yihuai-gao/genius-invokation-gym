from queue import PriorityQueue
from typing import TYPE_CHECKING, List, cast

from pydantic import BaseModel, validator

from gisim.classes.enums import *
from gisim.classes.message import (
    ElementalReactionTriggeredMsg,
    DealDamageMsg,
    UseSkillMsg,
    GenerateSummonMsg,
    GenerateCharacterStatusMsg,
    GenerateCombatStatusMsg,
)


if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Reaction(BaseModel):
    """元素反应"""
    id: int
    name: str
    reaction_type: ElementType
    increased_bonuses: int = 0
    """反应的（对伤害）增益:本伤害+2"""

    status_name: str = ""
    """为角色附加的效果，冻结"""
    status_remaining_round: int = 0
    status_remaining_usage: int = 0

    combat_status_name: str = ""
    """为阵营附加的效果 草原核 激化领域"""
    combat_status_remaining_round: int = 0
    combat_status_remaining_usage: int = 0

    piercing_damage_value: int = 0

    summon_name: str = ""
    """生成的召唤物"""

    def to_reaction(self, msg_queue: PriorityQueue, parent: "CharacterEntity"):
        # sourcery skip: low-code-quality
        player_id, parent_pos = parent.player_id, parent.position
        # 没有触发反应无需任何动作
        if self.reaction_type == ElementalReactionType.NONE:
            return None
        # 获取正在被处理的消息
        top_msg = msg_queue.queue[0]
        # 注意，元素反应不一定是伤害触发的，有时是效果触发的，技能触发，自身触发
        if isinstance(top_msg,UseSkillMsg):
            top_msg = cast(UseSkillMsg, top_msg)
            new_msg = ElementalReactionTriggeredMsg(
                elemental_reaction_type=self.reaction_type,
                target = (player_id, parent_pos),
                source = (player_id, parent_pos)
            )

        elif isinstance(top_msg, DealDamageMsg):
            # 由于伤害触发的
            top_msg = cast(DealDamageMsg, top_msg)
            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(top_msg.targets):
                if target_id == player_id and target_pos == parent_pos:
                    # 加伤 添加元素反应类型
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val + self.increased_bonuses,
                    )
                    new_msg = ElementalReactionTriggeredMsg(
                        elemental_reaction_type=self.reaction_type,
                        target = (player_id, parent_pos),
                        source = top_msg.attacker
                    )
                    attacker_id,attacker_pos = top_msg.attacker
                    if self.piercing_damage_value > 0:
                        new_msg = DealDamageMsg(
                            attack_type=AttackType.ELEMENTAL_REACTION,
                            attacker= top_msg.attacker,
                            sender_id= top_msg.attacker,
                            targets=[
                                (
                                    target_id,
                                    target_pos + k,
                                    ElementType.PIERCE,
                                    self.piercing_damage_value,
                                )
                                for k in [1, 2]  # Deals damage to two other characters
                            ],
                        )
                        msg_queue.put(new_msg)

                    if self.summon_name:
                        new_msg = GenerateSummonMsg(
                            sender_id=attacker_id , summon_name=self.summon_name
                        )
                        msg_queue.put(new_msg)

                    if self.status_name:
                        new_msg = GenerateCharacterStatusMsg(
                            sender_id=top_msg.attacker,
                            target=(parent.player_id, parent.position),
                            status_name=self.status_name,
                            remaining_round=self.status_remaining_round,
                            remaining_usage=self.status_remaining_usage,
                        )
                        msg_queue.put(new_msg)

                    if self.combat_status_name:
                        new_msg = GenerateCombatStatusMsg(
                            sender_id=top_msg.attacker,
                            target_player_id=parent.player_id,
                            combat_status_name=self.combat_status_name,
                            remaining_round=self.combat_status_remaining_round,
                            remaining_usage=self.combat_status_remaining_usage,
                        )
                        msg_queue.put(new_msg)
        msg_queue.put(new_msg)





import copy
from queue import PriorityQueue
from typing import TYPE_CHECKING, List, Tuple, cast

import numpy as np
from pydantic import BaseModel

from gisim.classes.enums import *
from gisim.classes.enums import ElementType
from gisim.classes.message import (
    DealDamageMsg,
    ElementalReactionTriggeredMsg,
    GenerateCharacterStatusMsg,
    GenerateCombatStatusMsg,
    GenerateSummonMsg,
    UseSkillMsg,
)
from gisim.classes.summon import AttackSummon

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity


RTE = np.zeros((8, 8), dtype="int")

"""草元素对应的行和列一定要靠后一些，最好位于最后一位，否则多元素反应会出现问题。
详情见https://github.com/hegugu-ng/genius-invokation-gym/blob/main/element_reaction_note.ipynb"""

FROZEN_VAL = [ElementType.HYDRO], [ElementType.CRYO], ElementalReactionType.FROZEN
"""冻结反应"""
MELT_VAL = [ElementType.PYRO], [ElementType.CRYO], ElementalReactionType.MELT
"""融化反应"""
SUPERCONDUCT_VAL = (
    [ElementType.ELECTRO],
    [ElementType.CRYO],
    ElementalReactionType.SUPERCONDUCT,
)
"""超导反应"""
VAPORIZE_VAL = [ElementType.PYRO], [ElementType.HYDRO], ElementalReactionType.VAPORIZE
"""蒸发反应"""
ELECTROCHARGED_VAL = (
    [ElementType.ELECTRO],
    [ElementType.HYDRO],
    ElementalReactionType.ELECTROCHARGED,
)
"""感电反应"""
OVERLOADED_VAL = (
    [ElementType.ELECTRO],
    [ElementType.PYRO],
    ElementalReactionType.OVERLOADED,
)
"""超载反应"""
BLOOM_VAL = [ElementType.DENDRO], [ElementType.HYDRO], ElementalReactionType.BLOOM
"""绽放反应"""
BURNING_VAL = [ElementType.DENDRO], [ElementType.PYRO], ElementalReactionType.BURNING
"""燃烧反应"""
QUICKEN_VAL = [ElementType.DENDRO], [ElementType.ELECTRO], ElementalReactionType.QUICKEN
"""激化反应"""
CRYSTALIZE_VAL = (
    [ElementType.GEO],
    [ElementType.CRYO, ElementType.HYDRO, ElementType.PYRO, ElementType.ELECTRO],
    ElementalReactionType.CRYSTALIZE,
)
"""结晶反应"""
SWIRL_VAL = (
    [ElementType.ANEMO],
    [ElementType.CRYO, ElementType.HYDRO, ElementType.PYRO, ElementType.ELECTRO],
    ElementalReactionType.SWIRL,
)
"""扩散反应"""

ATTACHMENT_GEO_VAL = [ElementType.GEO], [0], 1
"""岩元素不能附着"""
ATTACHMENT_ANEMO_VAL = [ElementType.ANEMO], [0], 1
"""风元素不能附着"""
ELEMENT_REACTION_MAP = [
    FROZEN_VAL,
    MELT_VAL,
    SUPERCONDUCT_VAL,
    VAPORIZE_VAL,
    ELECTROCHARGED_VAL,
    OVERLOADED_VAL,
    BLOOM_VAL,
    BURNING_VAL,
    QUICKEN_VAL,
    CRYSTALIZE_VAL,
    SWIRL_VAL,
    ATTACHMENT_GEO_VAL,
    ATTACHMENT_ANEMO_VAL,
]

REACTIONLIST_MAP = {
    ElementalReactionType.NONE: "CannotReaction",
    ElementalReactionType.BLOOM: "Bloom",
    ElementalReactionType.BURNING: "Burning",
    ElementalReactionType.CRYSTALIZE: "Crystalize",
    ElementalReactionType.ELECTROCHARGED: "ElectroCharged",
    ElementalReactionType.FROZEN: "Frozen",
    ElementalReactionType.MELT: "Melt",
    ElementalReactionType.OVERLOADED: "Overloaded",
    ElementalReactionType.QUICKEN: "Quicken",
    ElementalReactionType.SUPERCONDUCT: "Superconduct",
    ElementalReactionType.SWIRL: "Swirl",
    ElementalReactionType.VAPORIZE: "Vaporize",
}

for row, col, val in ELEMENT_REACTION_MAP:
    RTE[np.ix_(row, col)] = val

RTE = RTE + RTE.T - np.diag(RTE.diagonal())


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
    status_buff_type: StatusType = StatusType.ATTACK_BUFF

    combat_status_name: str = ""
    """为阵营附加的效果 草原核 激化领域"""
    combat_status_remaining_round: int = 0
    combat_status_remaining_usage: int = 0

    piercing_damage_value: int = 0

    summon_name: str = ""
    """生成的召唤物"""

    def to_reaction(
        self,
        msg_queue: PriorityQueue,
        parent: "CharacterEntity",
        reaction_tuple: Tuple[ElementType, ElementType],
    ):
        # sourcery skip: low-code-quality
        top_msg = msg_queue.queue[0]

        player_id, parent_pos = parent.player_id, parent.position
        if self.reaction_type == ElementalReactionType.NONE:
            return None
        typmsg = "By Self"
        if isinstance(top_msg, UseSkillMsg):
            top_msg = cast(UseSkillMsg, top_msg)
            new_msg = ElementalReactionTriggeredMsg(
                sender_id=parent.player_id,
                elemental_reaction_type=self.reaction_type,
                target=(parent.player_id, parent.position),
                source=(parent.player_id, parent.position),
                reaction_tuple=reaction_tuple,
            )
            typmsg = "By Self"
            msg_queue.put(new_msg)

        elif isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                top_msg.targets
            ):
                if target_id == player_id and target_pos == parent_pos:
                    top_msg.targets[idx] = (
                        target_id,
                        target_pos,
                        element_type,
                        dmg_val + self.increased_bonuses,
                    )
                    new_msg = ElementalReactionTriggeredMsg(
                        sender_id=player_id,
                        elemental_reaction_type=self.reaction_type,
                        target=(player_id, parent_pos),
                        source=top_msg.attacker,
                        reaction_tuple=reaction_tuple,
                    )
                    msg_queue.put(new_msg)
                    typmsg = "From Attack"
                    attacker_id, attacker_pos = top_msg.attacker
                    if self.piercing_damage_value > 0:
                        new_msg = DealDamageMsg(
                            attack_type=AttackType.ELEMENTAL_REACTION,
                            attacker=top_msg.attacker,
                            sender_id=top_msg.attacker,
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

        print(
            f"    Initiate Elemental Reactions:\n        Elemental Reaction :{self.reaction_type.name}\n        Target :{(player_id, parent_pos)}\n        Reaction Type:{typmsg}\n"
        )

        if self.summon_name:
            new_msg = GenerateSummonMsg(
                sender_id=attacker_id, summon_name=self.summon_name
            )
            msg_queue.put(new_msg)

        if self.status_name:
            new_msg = GenerateCharacterStatusMsg(
                sender_id=player_id,
                target=(parent.player_id, parent.position),
                status_name=self.status_name,
                remaining_round=self.status_remaining_round,
                remaining_usage=self.status_remaining_usage,
                status_type=self.status_buff_type,
            )
            msg_queue.put(new_msg)

        if self.combat_status_name:
            new_msg = GenerateCombatStatusMsg(
                sender_id=player_id,
                target_player_id=parent.player_id,
                combat_status_name=self.combat_status_name,
                remaining_round=self.combat_status_remaining_round,
                remaining_usage=self.combat_status_remaining_usage,
            )
            msg_queue.put(new_msg)


class Bloom(Reaction):
    """绽放"""

    id: int = 12
    name: str = "Bloom"
    effect_text: str = "Bloom: [Increased Bonuses]DMG +1 for this instance, [Character Status]creates a Dendro Core Buff Icon Dendro Core that grants +2 DMG to the next instance of Pyro/Electro DMG"
    reaction_type: ElementalReactionType = ElementalReactionType.BLOOM
    increased_bonuses: int = 1


class Burning(Reaction):
    """燃烧"""

    id: int = 18
    name: str = "Burning"
    effect_text: str = "Burning: [Increased Bonuses]DMG +1 for this instance, [Summon]creates a Burning Flame that will deal 1 Pyro DMG at the end of the Round (Takes effect once, max 2 stacks)"
    reaction_type: ElementalReactionType = ElementalReactionType.BURNING
    increased_bonuses: int = 1
    summon_name = "Burning Flame"


class BurningFlame(AttackSummon):
    """燃烧烈焰"""

    name: str = "Burning Flame"
    usages: int = 2
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2


class CannotReaction(Reaction):
    """无效果"""

    id: int = 0
    name: str = "CannotReaction"
    effect_text: str = (
        "CannotReaction: No elemental reactions have occurred and there is no effect"
    )
    reaction_type: ElementalReactionType = ElementalReactionType.NONE
    increased_bonuses: int = 0


class Crystalize(Reaction):
    """结晶"""

    id: int = 5
    name: str = "Crystallize"
    effect_text: str = "Crystallize: [Increased Bonuses]DMG +1 for this instance, [Combat Status]your active character gains 1 Shield point (Can stack, max 2 points)"
    reaction_type: ElementalReactionType = ElementalReactionType.CRYSTALIZE
    increased_bonuses: int = 1


class ElectroCharged(Reaction):
    """感电"""

    id: int = 8
    name: str = "ElectroCharged"
    effect_text: str = "Electro Charged: [Increased Bonuses]DMG +1 for this instance, [Piercing DMG]deal 1 Piercing DMG to all opposing characters except the target"
    reaction_type: ElementalReactionType = ElementalReactionType.ELECTROCHARGED
    increased_bonuses: int = 1


class Frozen(Reaction):
    """
    Frozen
    [Increased Bonuses]DMG +1 for this instance,
    [Character Status]the target is unable to perform any Actions this round
    (Can be removed in advance after the target receives Physical or Pyro DMG,
      in which case they will take +2 DMG)
    """

    id: int = 2
    name: str = "Frozen"
    effect_text: str = "Frozen: [Increased Bonuses]DMG +1 for this instance,[Character Status]the target is unable to perform any Actions this round (Can be removed in advance after the target receives Physical or Pyro DMG, in which case they will take +2 DMG)"
    reaction_type: ElementalReactionType = ElementalReactionType.FROZEN
    increased_bonuses: int = 1

    status_name: str = "Frozen Effect"
    status_remaining_round: int = 1
    status_remaining_usage: int = 1
    status_buff_type: StatusType = StatusType.UNDER_ATTACK_BUFF


class Melt(Reaction):
    """融化"""

    id: int = 3
    name: str = "Melt"
    effect_text: str = "Melt:[Increased Bonuses] Deal +2 DMG for this instance."
    reaction_type: ElementalReactionType = ElementalReactionType.MELT
    increased_bonuses: int = 2


class Overloaded(Reaction):
    """超载"""

    id: int = 9
    name: str = "Overloaded"
    effect_text: str = "Overloaded: [Increased Bonuses]DMG +2 for this instance, the target is forcibly switched to the next character"
    reaction_type: ElementalReactionType = ElementalReactionType.OVERLOADED
    increased_bonuses: int = 2


class Quicken(Reaction):
    """激化"""

    id: int = 24
    name: str = "Quicken"
    effect_text: str = "Quicken: [Increased Bonuses]DMG +1 for this instance, [Combat Status]creates a Catalyzing Field Buff Icon Catalyzing Field that grants +1 DMG to the next 2 instances of Dendro/Electro DMG"
    reaction_type: ElementalReactionType = ElementalReactionType.QUICKEN
    increased_bonuses: int = 1


class Superconduct(Reaction):
    """超导"""

    id: int = 4
    name: str = "Superconduct"
    effect_text: str = "Superconduct: [Increased Bonuses]DMG +1 for this instance, [Piercing DMG]deal 1 Piercing DMG to all opposing characters except the target"
    reaction_type: ElementalReactionType = ElementalReactionType.SUPERCONDUCT
    increased_bonuses: int = 1


class Swirl(Reaction):
    """扩散"""

    id: int = 7
    name: str = "Swirl"
    effect_text: str = "Swirl: Deals 1 DMG of the involved non-Anemo Element to all opposing characters except the target"
    reaction_type: ElementalReactionType = ElementalReactionType.SWIRL
    increased_bonuses: int = 0

    def to_reaction(
        self,
        msg_queue: PriorityQueue,
        parent: "CharacterEntity",
        reaction_tuple: Tuple[ElementType, ElementType],
    ):
        top_msg = msg_queue.queue[0]
        player_id, parent_pos = parent.player_id, parent.position
        if isinstance(top_msg, DealDamageMsg):
            top_msg = cast(DealDamageMsg, top_msg)
            for idx, (target_id, target_pos, element_type, dmg_val) in enumerate(
                top_msg.targets
            ):
                if target_id == player_id and target_pos == parent_pos:
                    new_msg = ElementalReactionTriggeredMsg(
                        sender_id=player_id,
                        elemental_reaction_type=self.reaction_type,
                        target=(player_id, parent_pos),
                        source=top_msg.attacker,
                        reaction_tuple=reaction_tuple,
                    )
                    msg_queue.put(new_msg)
                    new_msg = DealDamageMsg(
                        attack_type=AttackType.ELEMENTAL_REACTION,
                        attacker=(parent.player_id, parent.position),
                        sender_id=parent.player_id,
                        targets=[
                            (
                                target_id,
                                target_pos + k,
                                reaction_tuple[1],
                                1,
                            )
                            for k in [1, 2]  # Deals damage to two other characters
                        ],
                    )
                    msg_queue.put(new_msg)


class Vaporize(Reaction):
    """蒸发"""

    id: int = 6
    name: str = "Vaporize"
    effect_text: str = "Vaporize: [Increased Bonuses]DMG +2 for this instance"
    reaction_type: ElementalReactionType = ElementalReactionType.VAPORIZE
    increased_bonuses: int = 2


def can_attachable(element: ElementType) -> bool:
    """是否为可附着元素 `True` 可附着"""
    if element.value <= 0 or element.value >= 8:
        return False
    attachment = RTE[np.ix_([element], [0])].tolist()
    return attachment[0][0] == 0


def sum_element_reaction(
    ElementalAttachment: List[ElementType], AddElement: ElementType
) -> Tuple[ElementalReactionType, int]:
    """计算发生的元素反应"""
    reaction = RTE[np.ix_(ElementalAttachment, [AddElement])]
    multiple_reaction = dict(enumerate(np.nditer(reaction), start=0))
    multiple_reaction = {
        key: value for key, value in multiple_reaction.items() if value != 0
    }
    multiple_reaction = sorted(multiple_reaction.items(), key=lambda x: x[1])
    if len(multiple_reaction) == 0:
        return ElementalReactionType.NONE, 0
    index, reaction_type = multiple_reaction[0]
    return ElementalReactionType(reaction_type), index


def element_reaction(
    ElementalAttachment: List[ElementType], AddElement: ElementType
) -> Tuple[list, Reaction, Tuple[ElementType, EntityType]]:
    """进行元素反应"""
    ElementalAttachment = copy.deepcopy(ElementalAttachment)
    cannot_reaction = get_reaction_system_by_type(ElementalReactionType.NONE)
    if AddElement.value <= 0 or AddElement.value >= 8:
        return ElementalAttachment, cannot_reaction, ()
    if (
        ElementType.GEO in ElementalAttachment
        or ElementType.ANEMO in ElementalAttachment
    ):
        raise ValueError("There are non attachable elements in the attachment list")
    if AddElement in ElementalAttachment:
        # 挂已经附着的元素没有效果
        return ElementalAttachment, cannot_reaction, ()
    attachable = can_attachable(AddElement)
    if not ElementalAttachment and attachable:
        # 如果角色没有元素附着，且新挂的元素是可附着元素
        ElementalAttachment.append(AddElement)
        return ElementalAttachment, cannot_reaction, ()

    if not ElementalAttachment:
        # 如果角色没有元素附着，且新挂的元素是不可附着元素
        return ElementalAttachment, cannot_reaction, ()
    # 判断元素反应
    reaction_type, index = sum_element_reaction(ElementalAttachment, AddElement)
    # 获取反应的元素
    reaction_tuple = (AddElement, ElementalAttachment[index])
    if reaction_type == ElementalReactionType.NONE:
        if not attachable:
            return ElementalAttachment, cannot_reaction, ()
        ElementalAttachment.append(AddElement)
        return ElementalAttachment, cannot_reaction, ()
    ElementalAttachment.pop(index)
    reaction_effect = get_reaction_system_by_type(reaction_type)
    return ElementalAttachment, reaction_effect, reaction_tuple


def get_reaction_system(reaction_name: str):
    """通过反应名称查找反应体系"""
    reaction_name = reaction_name.replace(" ", "").replace("'", "")
    reaction_system_class = globals()[reaction_name]
    reaction_system: Reaction = reaction_system_class()
    return reaction_system


def get_reaction_system_by_type(reaction_type: ElementalReactionType):
    """通过反应类型查找反应体系"""
    reaction_name = REACTIONLIST_MAP[reaction_type]
    return get_reaction_system(reaction_name)

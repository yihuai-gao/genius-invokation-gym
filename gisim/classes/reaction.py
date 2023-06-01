from gisim.classes.enums import *
from gisim.classes.entity import Entity
import numpy as np
from enum import IntEnum
from typing import List
from gisim.ElementalReaction import get_reaction_system, get_reaction_system_by_type
from gisim.ElementalReaction.base import Reaction


RTE = np.zeros((8, 8), dtype="int")

FROZEN_VAL = [ElementType.HYDRO], [ElementType.CRYO], ReactionType.FROZEN
MELT_VAL = [ElementType.PYRO], [ElementType.CRYO], ReactionType.MELT
SUPERCONDUCT_VAL = [ElementType.ELECTRO], [
    ElementType.CRYO], ReactionType.SUPERCONDUCT
VAPORIZE_VAL = [ElementType.PYRO], [ElementType.HYDRO], ReactionType.VAPORIZE
ELECTROCHARGED_VAL = [ElementType.ELECTRO], [
    ElementType.HYDRO], ReactionType.ELECTROCHARGED
OVERLOADED_VAL = [ElementType.ELECTRO], [
    ElementType.PYRO], ReactionType.OVERLOADED
BLOOM_VAL = [ElementType.DENDRO], [ElementType.HYDRO], ReactionType.BLOOM
BURNING_VAL = [ElementType.DENDRO], [ElementType.PYRO], ReactionType.BURNING
QUICKEN_VAL = [ElementType.DENDRO], [ElementType.ELECTRO], ReactionType.QUICKEN
CRYSTALLIZE_VAL = [ElementType.GEO], [ElementType.CRYO, ElementType.HYDRO,
                                      ElementType.PYRO, ElementType.ELECTRO], ReactionType.CRYSTALLIZE
SWIRL_VAL = [ElementType.ANEMO], [ElementType.CRYO, ElementType.HYDRO,
                                  ElementType.PYRO, ElementType.ELECTRO], ReactionType.SWIRL

ATTACHMENT_GEO_VAL = [ElementType.GEO], [0], 1
ATTACHMENT_ANEMO_VAL = [ElementType.ANEMO], [0], 1
ELEMENT_REACTION_MAP = [FROZEN_VAL, MELT_VAL, SUPERCONDUCT_VAL, VAPORIZE_VAL, ELECTROCHARGED_VAL, OVERLOADED_VAL,
                        BLOOM_VAL, BURNING_VAL, QUICKEN_VAL, CRYSTALLIZE_VAL, SWIRL_VAL, ATTACHMENT_GEO_VAL, ATTACHMENT_ANEMO_VAL]


for row, col, val in ELEMENT_REACTION_MAP:
    RTE[np.ix_(row, col)] = val

RTE = RTE + RTE.T - np.diag(RTE.diagonal())


def can_attachable(element: ElementType) -> bool:
    """是否为可附着元素 `True` 可附着"""
    attachment = RTE[np.ix_([element], [0])].tolist()
    return attachment[0][0] == 0


def sum_element_reaction(ElementalAttachment: List[ElementType], AddElement: ElementType) -> tuple[ReactionType, int]:
    """计算发生的元素反应"""
    reaction = RTE[np.ix_(ElementalAttachment, [AddElement])]
    multiple_reaction = dict(enumerate(np.nditer(reaction), start=0))
    multiple_reaction = {key: value for key, value in multiple_reaction.items() if value != 0}
    multiple_reaction = sorted(multiple_reaction.items(), key=lambda x: x[1])
    if len(multiple_reaction) == 0:
        return ReactionType.NONE,0
    index, reaction_type = multiple_reaction[0]
    return ReactionType(reaction_type), index


def element_reaction(ElementalAttachment: List[ElementType], AddElement: ElementType) -> tuple[list, Reaction]:
    if ElementType.GEO in ElementalAttachment or ElementType.ANEMO in ElementalAttachment:
        raise ValueError("There are non attachable elements in the attachment list")
    if AddElement in ElementalAttachment:
        # 挂已经附着的元素没有效果
        return ElementalAttachment, None
    attachable = can_attachable(AddElement)
    if not ElementalAttachment and attachable:
        # 如果角色没有元素附着，且新挂的元素是可附着元素
        ElementalAttachment.append(AddElement)
        return ElementalAttachment, None

    if not ElementalAttachment:
        # 如果角色没有元素附着，且新挂的元素是不可附着元素
        return ElementalAttachment, None
    # 判断元素反应
    reaction_type, index = sum_element_reaction(
        ElementalAttachment, AddElement)
    if reaction_type == ReactionType.NONE:
        if not attachable:
            return ElementalAttachment, None
        ElementalAttachment.append(AddElement)
        return ElementalAttachment, None
    # 发生了元素反应产生效果 获取效果
    ElementalAttachment.pop(index)
    reaction_effect = get_reaction_system_by_type(reaction_type)
    return ElementalAttachment, reaction_effect

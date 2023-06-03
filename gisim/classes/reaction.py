from gisim.classes.enums import *
import numpy as np
from typing import List
from gisim.elementalReaction import get_reaction_system, get_reaction_system_by_type
from gisim.elementalReaction.base import Reaction
import copy


RTE = np.zeros((8, 8), dtype="int")

"""草元素对应的行和列一定要靠后一些，最好位于最后一位，否则多元素反应会出现问题。
详情见https://github.com/hegugu-ng/genius-invokation-gym/blob/main/element_reaction_note.ipynb"""

FROZEN_VAL = [ElementType.HYDRO], [ElementType.CRYO], ElementalReactionType.FROZEN
"""冻结反应"""
MELT_VAL = [ElementType.PYRO], [ElementType.CRYO], ElementalReactionType.MELT
"""融化反应"""
SUPERCONDUCT_VAL = [ElementType.ELECTRO], [ElementType.CRYO], ElementalReactionType.SUPERCONDUCT
"""超导反应"""
VAPORIZE_VAL = [ElementType.PYRO], [ElementType.HYDRO], ElementalReactionType.VAPORIZE
"""蒸发反应"""
ELECTROCHARGED_VAL = [ElementType.ELECTRO], [ElementType.HYDRO], ElementalReactionType.ELECTROCHARGED
"""感电反应"""
OVERLOADED_VAL = [ElementType.ELECTRO], [ElementType.PYRO], ElementalReactionType.OVERLOADED
"""超载反应"""
BLOOM_VAL = [ElementType.DENDRO], [ElementType.HYDRO], ElementalReactionType.BLOOM
"""绽放反应"""
BURNING_VAL = [ElementType.DENDRO], [ElementType.PYRO], ElementalReactionType.BURNING
"""燃烧反应"""
QUICKEN_VAL = [ElementType.DENDRO], [ElementType.ELECTRO], ElementalReactionType.QUICKEN
"""激化反应"""
CRYSTALIZE_VAL = [ElementType.GEO], [ElementType.CRYO, ElementType.HYDRO, ElementType.PYRO, ElementType.ELECTRO], ElementalReactionType.CRYSTALIZE
"""结晶反应"""
SWIRL_VAL = [ElementType.ANEMO], [ElementType.CRYO, ElementType.HYDRO, ElementType.PYRO, ElementType.ELECTRO], ElementalReactionType.SWIRL
"""扩散反应"""

ATTACHMENT_GEO_VAL = [ElementType.GEO], [0], 1
"""岩元素不能附着"""
ATTACHMENT_ANEMO_VAL = [ElementType.ANEMO], [0], 1
"""风元素不能附着"""
ELEMENT_REACTION_MAP = [FROZEN_VAL, MELT_VAL, SUPERCONDUCT_VAL, VAPORIZE_VAL, ELECTROCHARGED_VAL, OVERLOADED_VAL, BLOOM_VAL, BURNING_VAL, QUICKEN_VAL, CRYSTALIZE_VAL, SWIRL_VAL, ATTACHMENT_GEO_VAL, ATTACHMENT_ANEMO_VAL]


for row, col, val in ELEMENT_REACTION_MAP:
    RTE[np.ix_(row, col)] = val

RTE = RTE + RTE.T - np.diag(RTE.diagonal())


def can_attachable(element: ElementType) -> bool:
    """是否为可附着元素 `True` 可附着"""
    if element.value <= 0 or element.value >= 8:
        # 草，为什么伤害类型会算到元素类型里面，我建议为了方便伤害的结算，建议给伤害做个类。
        return False
    attachment = RTE[np.ix_([element], [0])].tolist()
    return attachment[0][0] == 0


def sum_element_reaction(ElementalAttachment: List[ElementType], AddElement: ElementType) -> tuple[ElementalReactionType, int]:
    """计算发生的元素反应"""
    reaction = RTE[np.ix_(ElementalAttachment, [AddElement])]
    multiple_reaction = dict(enumerate(np.nditer(reaction), start=0))
    multiple_reaction = {key: value for key, value in multiple_reaction.items() if value != 0}
    multiple_reaction = sorted(multiple_reaction.items(), key=lambda x: x[1])
    if len(multiple_reaction) == 0:
        return ElementalReactionType.NONE,0
    index, reaction_type = multiple_reaction[0]
    return ElementalReactionType(reaction_type), index


def element_reaction(ElementalAttachment: List[ElementType], AddElement: ElementType) -> tuple[list, Reaction]:
    """进行元素反应"""
    ElementalAttachment = copy.deepcopy(ElementalAttachment)
    cannot_reaction = get_reaction_system_by_type(ElementalReactionType.NONE)
    if AddElement.value <= 0 or AddElement.value >= 8:
        # 草，为什么伤害类型会算到元素类型里面，我建议为了方便伤害的结算，建议给伤害做个类。
        return ElementalAttachment,cannot_reaction
    if ElementType.GEO in ElementalAttachment or ElementType.ANEMO in ElementalAttachment:
        raise ValueError("There are non attachable elements in the attachment list")
    if AddElement in ElementalAttachment:
        # 挂已经附着的元素没有效果
        return ElementalAttachment, cannot_reaction
    attachable = can_attachable(AddElement)
    if not ElementalAttachment and attachable:
        # 如果角色没有元素附着，且新挂的元素是可附着元素
        ElementalAttachment.append(AddElement)
        return ElementalAttachment, cannot_reaction

    if not ElementalAttachment:
        # 如果角色没有元素附着，且新挂的元素是不可附着元素
        return ElementalAttachment, cannot_reaction
    # 判断元素反应
    reaction_type, index = sum_element_reaction(
        ElementalAttachment, AddElement)
    if reaction_type == ElementalReactionType.NONE:
        if not attachable:
            return ElementalAttachment, cannot_reaction
        ElementalAttachment.append(AddElement)
        return ElementalAttachment, cannot_reaction
    # 发生了元素反应产生效果 获取效果
    ElementalAttachment.pop(index)
    reaction_effect = get_reaction_system_by_type(reaction_type)
    return ElementalAttachment, reaction_effect

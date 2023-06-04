from .bloom import *
from .burning import *
from .crystalize import *
from .electro_charged import *
from .frozen import *
from .melt import *
from .overloaded import *
from .quicken import *
from .superconduct import *
from .swirl import *
from .vaporize import *
from .base import *
from .cannot_reaction import *

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

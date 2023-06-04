"""无效果"""
from gisim.classes.enums import *
from gisim.elemental_reaction.base import Reaction



class CannotReaction(Reaction):
    """无效果"""
    id: int = 0
    name: str = "CannotReaction"
    effect_text: str = "CannotReaction: No elemental reactions have occurred and there is no effect"
    reaction_type: ElementalReactionType = ElementalReactionType.NONE
    increased_bonuses: int = 0

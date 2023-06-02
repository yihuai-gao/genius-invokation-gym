"""融化"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Melt(Reaction):
    """融化"""
    id: int = 3
    name: str = "Melt"
    effect_text: str = "Melt:[Increased Bonuses] Deal +2 DMG for this instance."
    reaction_type: ReactionType = ReactionType.MELT
    increased_bonuses: int = 2

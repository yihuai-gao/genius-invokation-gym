"""超载"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Overloaded(Reaction):
    """超载"""
    id: int = 9
    name: str = "Overloaded"
    effect_text: str = "Overloaded: [Increased Bonuses]DMG +2 for this instance, the target is forcibly switched to the next character"
    reaction_type: ReactionType = ReactionType.OVERLOADED
    increased_bonuses: int = 2

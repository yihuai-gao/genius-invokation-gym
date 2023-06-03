"""扩散"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.elementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Swirl(Reaction):
    """扩散"""
    id: int = 7
    name: str = "Swirl"
    effect_text: str = "Swirl: Deals 1 DMG of the involved non-Anemo Element to all opposing characters except the target"
    reaction_type: ElementalReactionType = ElementalReactionType.SWIRL
    increased_bonuses: int = 0

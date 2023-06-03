"""蒸发"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.elementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Vaporize(Reaction):
    """蒸发"""
    id: int = 6
    name: str = "Vaporize"
    effect_text: str = "Vaporize: [Increased Bonuses]DMG +2 for this instance"
    reaction_type: ElementalReactionType = ElementalReactionType.VAPORIZE
    increased_bonuses: int = 2

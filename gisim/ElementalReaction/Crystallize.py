"""结晶"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Crystallize(Reaction):
    """结晶"""
    id: int = 5
    name: str = "Crystallize"
    effect_text: str = "Crystallize: [Increased Bonuses]DMG +1 for this instance, [Combat Status]your active character gains 1 Shield point (Can stack, max 2 points)"
    reaction_type: ReactionType = ReactionType.CRYSTALLIZE
    main_element: ElementType = ElementType.GEO
    secondary_element: List[ElementType] = []
    increased_bonuses: int = 1

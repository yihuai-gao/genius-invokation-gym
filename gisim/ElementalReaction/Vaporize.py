"""蒸发"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Vaporize(Reaction):
    """蒸发"""
    id: int = 6
    name: str = "Vaporize"
    effect_text: str = "Vaporize: [Increased Bonuses]DMG +2 for this instance"
    reaction_type: ReactionType = ReactionType.VAPORIZE
    main_element: ElementType = ElementType.HYDRO
    secondary_element: List[ElementType] = [ElementType.PYRO]
    increased_bonuses: int = 2

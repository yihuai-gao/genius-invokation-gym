"""冻结"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Frozen(Reaction):
    """冻结"""
    id: int = 2
    name: str = "Frozen"
    effect_text: str = "Frozen: [Increased Bonuses]DMG +1 for this instance, [Character Status]the target is unable to perform any Actions this round (Can be removed in advance after the target receives Physical or Pyro DMG, in which case they will take +2 DMG)"
    reaction_type: ReactionType = ReactionType.FROZEN
    main_element: ElementType = ElementType.CRYO
    secondary_element: List[ElementType] = [ElementType.HYDRO]
    increased_bonuses: int = 1

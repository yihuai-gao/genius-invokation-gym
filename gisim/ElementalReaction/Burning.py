"""燃烧"""
from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Burning(Reaction):
    """燃烧"""
    id: int = 18
    name: str = "Burning"
    effect_text: str = "Burning: [Increased Bonuses]DMG +1 for this instance, [Summon]creates a Burning Flame that will deal 1 Pyro DMG at the end of the Round (Takes effect once, max 2 stacks)"
    reaction_type: ReactionType = ReactionType.BURNING
    main_element: ElementType = ElementType.PYRO
    secondary_element: List[ElementType] = [ElementType.DENDRO]
    increased_bonuses: int = 1

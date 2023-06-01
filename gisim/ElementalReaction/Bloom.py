"""绽放"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Bloom(Reaction):
    """绽放"""
    id: int = 12
    name: str = "Bloom"
    effect_text: str = "Bloom: [Increased Bonuses]DMG +1 for this instance, [Character Status]creates a Dendro Core Buff Icon Dendro Core that grants +2 DMG to the next instance of Pyro/Electro DMG"
    reaction_type: ReactionType = ReactionType.BLOOM
    main_element: ElementType = ElementType.DENDRO
    secondary_element: List[ElementType] = [ElementType.HYDRO]
    increased_bonuses: int = 1

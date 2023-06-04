"""激化"""

from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.elemental_reaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Quicken(Reaction):
    """激化"""
    id: int = 24
    name: str = "Quicken"
    effect_text: str = "Quicken: [Increased Bonuses]DMG +1 for this instance, [Combat Status]creates a Catalyzing Field Buff Icon Catalyzing Field that grants +1 DMG to the next 2 instances of Dendro/Electro DMG"
    reaction_type: ElementalReactionType = ElementalReactionType.QUICKEN
    increased_bonuses: int = 1

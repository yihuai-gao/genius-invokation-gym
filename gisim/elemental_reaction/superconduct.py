"""超导"""
from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.elemental_reaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Superconduct(Reaction):
    """超导"""
    id: int = 4
    name: str = "Superconduct"
    effect_text: str = "Superconduct: [Increased Bonuses]DMG +1 for this instance, [Piercing DMG]deal 1 Piercing DMG to all opposing characters except the target"
    reaction_type: ElementalReactionType = ElementalReactionType.SUPERCONDUCT
    increased_bonuses: int = 1

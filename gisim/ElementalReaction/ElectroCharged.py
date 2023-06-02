"""感电"""
from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class ElectroCharged(Reaction):
    """感电"""
    id: int = 8
    name: str = "ElectroCharged"
    effect_text: str = "Electro Charged: [Increased Bonuses]DMG +1 for this instance, [Piercing DMG]deal 1 Piercing DMG to all opposing characters except the target"
    reaction_type: ReactionType = ReactionType.ELECTROCHARGED
    increased_bonuses: int = 1

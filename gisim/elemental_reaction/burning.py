"""燃烧"""
from typing import TYPE_CHECKING, List

from gisim.classes.enums import *
from gisim.elemental_reaction.base import Reaction

from gisim.classes.summon import AttackSummon

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Burning(Reaction):
    """燃烧"""
    id: int = 18
    name: str = "Burning"
    effect_text: str = "Burning: [Increased Bonuses]DMG +1 for this instance, [Summon]creates a Burning Flame that will deal 1 Pyro DMG at the end of the Round (Takes effect once, max 2 stacks)"
    reaction_type: ElementalReactionType = ElementalReactionType.BURNING
    increased_bonuses: int = 1
    summon_name = "Burning Flame"


class BurningFlame(AttackSummon):
    """ 燃烧烈焰"""
    name: str = "Burning Flame"
    usages: int = 2
    damage_element: ElementType = ElementType.CRYO
    damage_value: int = 2

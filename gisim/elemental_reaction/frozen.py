"""冻结"""

from typing import TYPE_CHECKING, List, cast
from queue import PriorityQueue

from gisim.classes.enums import *
from gisim.elemental_reaction.base import Reaction
from gisim.classes.status import CharacterStatusEntity

from gisim.classes.message import (
    ChangeCharacterMsg,
    DealDamageMsg,
    GenerateCharacterStatusMsg,
    GenerateEquipmentMsg,
    Message,
    PayChangeCharacterCostMsg,
    RoundEndMsg,
    UseCardMsg,
)

if TYPE_CHECKING:
    from gisim.classes.character import CharacterEntity
    from gisim.game import GameInfo


class Frozen(Reaction):
    """
    Frozen
    [Increased Bonuses]DMG +1 for this instance,
    [Character Status]the target is unable to perform any Actions this round 
    (Can be removed in advance after the target receives Physical or Pyro DMG,
      in which case they will take +2 DMG)
    """
    id: int = 2
    name: str = "Frozen"
    effect_text: str = "Frozen: [Increased Bonuses]DMG +1 for this instance,[Character Status]the target is unable to perform any Actions this round (Can be removed in advance after the target receives Physical or Pyro DMG, in which case they will take +2 DMG)"
    reaction_type: ElementalReactionType = ElementalReactionType.FROZEN
    increased_bonuses: int = 1

    status_name: str = "Frozen Effect"
    status_remaining_round: int = 1
    status_remaining_usage: int = 1
    status_buff_type: StatusType = StatusType.UNDER_ATTACK_BUFF




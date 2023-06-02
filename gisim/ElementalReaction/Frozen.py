"""冻结"""

from typing import TYPE_CHECKING, List,cast
from queue import PriorityQueue

from gisim.classes.enums import *
from gisim.ElementalReaction.base import Reaction

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
    """冻结"""
    id: int = 2
    name: str = "Frozen"
    effect_text: str = "Frozen: [Increased Bonuses]DMG +1 for this instance, [Character Status]the target is unable to perform any Actions this round (Can be removed in advance after the target receives Physical or Pyro DMG, in which case they will take +2 DMG)"
    reaction_type: ReactionType = ReactionType.FROZEN
    increased_bonuses: int = 1

    def to_reaction(self, msg_queue: PriorityQueue,player_id: PlayerID, parent: "CharacterEntity"):
        """[Character Status]the target is unable to perform any Actions this round
          (Can be removed in advance after the target receives Physical or Pyro DMG, in which case they will take +2 DMG)"""
        new_msg = GenerateCharacterStatusMsg(
            sender_id=parent.player_id,
            status_name="Frozen Effect",
            target=(parent.player_id, parent.position),
            remaining_round=1,
            remaining_usage=999,
        )
        msg_queue.put(new_msg)


        


from abc import ABC, abstractmethod

from classes.enums import CharacterPosition, PlayerID

from .entity import Entity


class CharacterStatusEntity(Entity, ABC):
    def __init__(self, name: str, player_id: PlayerID, position: CharacterPosition):
        """Status which is attached to a fixed character.
        Shown in the upper line of the character card. Will be calculated earlier."""
        super().__init__()
        self.player_id = player_id
        self.position = position
        self.name = name

    def encode(self):
        # TODO
        pass


class CombatStatusEntity(Entity, ABC):
    """Status which is attached dynamically to the active character.
    Shown in the lower line of the character card. Will be calculated later."""

    def __init__(self, name: str, player_id: PlayerID):
        super().__init__()
        self.player_id = player_id
        self.name = name

    def encode(self):
        # TODO
        pass

from abc import ABC, abstractmethod

from .entity import Entity


class Support(Entity, ABC):
    def __init__(self, name: str, player_id: int):
        super().__init__()
        assert player_id in [1, 2]
        self.player_id = player_id
        self.name = name

    def encode(self):
        # TODO
        pass

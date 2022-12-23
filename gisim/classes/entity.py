"""The most basic class for all elements in the game
"""
import logging
from queue import PriorityQueue
from typing import TYPE_CHECKING
import uuid
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from gisim.classes.message import Message


class Entity(ABC):
    def __init__(self):
        self._uuid = uuid.uuid4()
        self._logger = logging.getLogger("gisim")
        
    # @abstractmethod
    def encode(self) -> dict:
        ...
        
    # @abstractmethod
    def msg_handler(self, msg_queue:PriorityQueue["Message"]) -> bool:
        """Return value should be a boolean to indicate whether the message queue is updated"""
        ...
        
class TalentEntity(Entity):
    def __init__(self, name:str):
        self.name = name
    
    def encode(self):
        return {"name": self.name}

    def msg_handler(self, msg_queue: PriorityQueue["Message"]) -> bool:
        updated = False
        return updated


class WeaponEntity(Entity):
    def __init__(self, name:str):
        self.name = name
        
    def encode(self):
        return {"name": self.name}

    def msg_handler(self, msg_queue: PriorityQueue["Message"]) -> bool:
        updated = False
        return updated
    
class ArtifactEntity(Entity):
    def __init__(self, name:str):
        self.name = name
        
    def encode(self):
        return {"name": self.name}

    def msg_handler(self, msg_queue: PriorityQueue["Message"]) -> bool:
        updated = False
        return updated
    
    
class StatusEntity(Entity):
    def __init__(self, name:str):
        self.name = name
        
    def encode(self):
        return {"name": self.name}

    def msg_handler(self, msg_queue: PriorityQueue["Message"]) -> bool:
        updated = False
        return updated
    
    
class CardEntity(Entity):
    def __init__(self, name: str):
        self.name = name
        self.enabled = True

        # TODO: Initialize card cost and other requirements based on their description

    def encode(self):
        ...
        
    def msg_handler(self, msg_queue: PriorityQueue["Message"]) -> bool:
        ...
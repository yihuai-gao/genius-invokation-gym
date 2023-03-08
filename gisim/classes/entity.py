"""The most basic class for all elements in the game
"""
from abc import ABC, abstractmethod
from logging import Logger, getLogger
from queue import PriorityQueue
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PrivateAttr

if TYPE_CHECKING:
    from gisim.classes.message import Message


class Entity(BaseModel, ABC):
    _uuid: UUID = PrivateAttr(default_factory=uuid4)
    # _logger: Logger = PrivateAttr(default_factory=getLogger("gisim"))

    def encode(self) -> dict:
        ...

    # @abstractmethod
    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        # PriorityQueue["Message"]
        """Return value should be a boolean to indicate whether the message queue is updated"""
        ...

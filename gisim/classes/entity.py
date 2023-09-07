"""The most basic class for all elements in the game
"""
from abc import ABC, abstractmethod
from itertools import count
from logging import Logger, getLogger
from queue import PriorityQueue
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, PrivateAttr

if TYPE_CHECKING:
    from gisim.classes.message import Message

counter = lambda c=count(): next(c)


class Entity(BaseModel, ABC):
    _uuid: UUID = PrivateAttr(default_factory=uuid4)
    # _logger: Logger = PrivateAttr(default_factory=getLogger("gisim"))

    time_tag: int = Field(default_factory=counter)
    respond_to_earlier_msg: bool = False
    """Whether this status will respond to a message that have a smaller time tag."""

    def encode(self) -> dict:
        ...

    # @abstractmethod
    def msg_handler(self, msg_queue: PriorityQueue) -> bool:
        # PriorityQueue["Message"]
        """Return value should be a boolean to indicate whether the message queue is updated"""
        ...

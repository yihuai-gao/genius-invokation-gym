"""The most basic class for all elements in the game
"""
import logging
import uuid
from abc import ABC


class Entity(ABC):
    def __init__(self):
        self._uuid = uuid.uuid4()
        self._logger = logging.getLogger("gisim")

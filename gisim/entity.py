'''The most basic class for all elements in the game
'''
from abc import ABCMeta
import uuid
import logging
class Entity(ABCMeta):
    def __init__(self):
        self._uuid = uuid.uuid4()
        self._logger = logging.getLogger("gisim")
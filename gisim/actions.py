''' Implement of all kinds of action:
Combat Action: Use Skill, Switch Characters, Declare End
Fast Action: Play Card, Elemental Tuning
'''

from .entity import Entity

class Action(Entity):
    def __init__(self, type:str, info:dict):
        self._type = type
        self._info = info
        
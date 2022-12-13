'''Abstract base class of card entities, initialized from its name'''

from gisim.classes.entity import Entity

class CardEntity(Entity):
    
    def __init__(self, name:str):
        self.name = name
        self.enabled = True

        # TODO: Initialize card cost and other requirements based on their description
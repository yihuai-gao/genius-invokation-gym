'''Base class of each character: abstract class
A character in the game should be an instant of the specific character class defined in each file'''
from ...entity import Entity
from abc import ABCMeta, abstractmethod

class Character(Entity, ABCMeta):
    def __init__(self, player_id:int, position:int):
        super().__init__()
        assert player_id in [1, 2], "The player_id should be either 1 or 2"
        assert position in [0, 1, 2], "The position should be on of 0(left), 1(middle), 2(right)"
        self.player_id = player_id
        self.position = position
        self.active = False 
        ''' Whether this character in set forward. There should be only one character in the active state for each player'''
        
    @property
    @abstractmethod
    def nationality(self):
        '''Should be either one of `Mondstadt`(蒙德), `Liyue`(璃月), `Inazuma`(稻妻), `Sumeru`(稻妻)'''
        ...
        
    @property
    @abstractmethod
    def weapon_type(self):
        '''Should be either one of `bow`(弓), `claymore`(单手剑), `sword`(双手剑), `polearm`(枪), `catalyst`(法器)'''
        ...

class Skill(ABCMeta):
    def __init__(self, cost:dict, passive=False):
        '''
        Args:
        cost(dict[str, int]): key: element type(including 'Arbitrary'), cost, empty if no cost is required 
        passive(bool): passive skill which can only be triggered
        '''

        self.cost = cost
        self.passive = passive
        
    @property
    @abstractmethod
    def requirements(self):
        '''Description of the requirement of the skill in domain-specific language (dsl)'''
        ...
        
    @property
    @abstractmethod
    def targets(self):
        '''Description of the target of the skill in domain-specific language (dsl)
        Use a list to assign multiple targets
        '''
        ...
        
    @property
    @abstractmethod
    def effects(self):
        '''Description of the target of the skill in domain-specific language (dsl)
        Use a list to assign multiple effects to the targets respectively'''
        ...
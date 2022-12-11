'''Base class of each character: abstract class
A character in the game should be an instant of the specific character class defined in each file'''
from .entity import Entity
from abc import ABCMeta, abstractmethod

class Character(Entity, ABCMeta):
    def __init__(self, name:str, player_id:int, position:int):
        super().__init__()
        assert player_id in [1, 2], "The player_id should be either 1 or 2"
        assert position in [0, 1, 2], "The position should be on of 0(left), 1(middle), 2(right)"
        self.PLAYER_ID = player_id
        self.POSITION = position
        self.NAME = name
        self.active = False 
        ''' Whether this character in set forward. There should be only one character in the active state for each player'''
        self.elemental_infusion = None
        '''普通攻击元素附魔'''
        self.elemental_attachment = None
        '''角色元素附着'''
    
    
    def get_raw_skill(self, id=None, skill_name=None, skill_type=None):
        '''Get the character's skill through either id (0, 1, 2, ...), name (str), or skill_type
        Returns:
            raw_skill (Skill): a Skill object with raw cost and effects (has not been affected by any discounts/enhancement)
        '''
        if id is not None:
            assert 0 <= id <= self.skills_num - 1, f"id should be from 0 to {self.skills_num-1}"
            return self.skills[id]
        elif skill_name is not None:
            if skill_name in self.SKILL_NAMES:
                return self.skills[self.SKILL_NAMES.index(skill_name)]
            else:
                assert False, f"Skill {skill_name} does not exist in {self.NAME}'s skill set"
        else:
            assert skill_type is not None, "Should provide either skill id or its name"

    def encode(self):
        # TODO
        pass
    
    @abstractmethod
    def get_all_raw_skills(self):
        '''
        Returns:
            all_raw_skill (list[Skill]): a list with all skills
        '''
        ...
    
    @property
    @abstractmethod
    def NATIONALITY(self):
        '''Should be either one of `Mondstadt`(蒙德), `Liyue`(璃月), `Inazuma`(稻妻), `Sumeru`(须弥)'''
        self.NATIONALITY:str
        ...
        
    @property
    @abstractmethod
    def WEAPON_TYPE(self):
        '''Should be either one of `bow`(弓), `claymore`(双手剑), `sword`(单手剑), `polearm`(枪), `catalyst`(法器)'''
        self.WEAPON_TYPE:str
        ...
    
    @property
    @abstractmethod
    def health_point(self):
        health_point:int
        ...
        
    @property
    @abstractmethod
    def SKILLS_NUM(self):
        self.SKILLS_NUM:int
        ...
        
    @property
    @abstractmethod
    def skills(self):
        self.skills:list[Skill]
        ...
        
    @property
    @abstractmethod
    def SKILL_NAMES(self):
        self.SKILL_NAMES:list[str]
        ...
        
    @property
    @abstractmethod
    def SKILL_NAMES(self):
        self.SKILL_NAMES:list[str]
        ...
        

class Skill(ABCMeta):
    def __init__(self, name:str, cost:dict, skill_type:str):
        '''
        Args:
        cost(dict[str, int]): {element dice type(including 'Arbitrary', 'Power'):cost}; None if no cost is required 
        passive(bool): passive skill which can only be triggered
        '''
        skill_types = ['Normal Attack', 'Elemental Skill', 'Elemental Burst', 'Passive Skill']
        assert skill_type in skill_types, f"Skill should be one of {skill_types}, but got {skill_type}."
        self.AME = name
        self.RAW_COST = cost
        self.TYPE = skill_type
        self.current_cost = cost
        
    @property
    @abstractmethod
    def requirements(self):
        '''Description of the requirement of the skill in domain-specific language (dsl).'''
        ...
        
    @property
    @abstractmethod
    def targets(self):
        '''Description of the target of the skill in domain-specific language (dsl).
        Use a list to assign multiple targets.
        '''
        ...
        
    @property
    @abstractmethod
    def effects(self):
        '''Description of the target of the skill in domain-specific language (dsl).
        Use a list to assign multiple effects to the targets respectively.'''
        ...
        
    
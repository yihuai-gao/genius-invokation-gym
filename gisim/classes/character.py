"""Base class of each character: abstract class
A character in the game should be an instant of the specific character class defined in each file"""
from abc import ABCMeta, abstractmethod

from gisim.classes.enums import *

from .entity import Entity


class Character(Entity, ABCMeta):
    def __init__(self, name: str, player_id: PlayerID, position: Position):
        super().__init__()
        self.PLAYER_ID = player_id
        self.POSITION = position
        self.NAME = name
        self.active = False
        """ Whether this character in set forward. There should be only one character in the active state for each player"""
        self.elemental_infusion = None
        """普通攻击元素附魔"""
        self.elemental_attachment = None
        """角色元素附着"""

    def get_raw_skill(self, id=None, skill_name=None, skill_type=None):
        """Get the character's skill through either id (0, 1, 2, ...), name (str), or skill_type
        Returns:
            raw_skill (Skill): a Skill object with raw cost and effects (has not been affected by any discounts/enhancement)
        """
        if id is not None:
            assert (
                0 <= id <= self.SKILL_NUM - 1
            ), f"id should be from 0 to {self.SKILL_NUM-1}"
            return self.skills[id]
        elif skill_name is not None:
            if skill_name in self.SKILL_NAMES:
                return self.skills[self.SKILL_NAMES.index(skill_name)]
            else:
                assert (
                    False
                ), f"Skill {skill_name} does not exist in {self.NAME}'s skill set"
        else:
            assert skill_type is not None, "Should provide either skill id or its name"

    def encode(self):
        # TODO
        pass

    @abstractmethod
    def get_all_raw_skills(self):
        """
        Returns:
            all_raw_skill (list[Skill]): a list with all skills
        """
        ...

    @property
    @abstractmethod
    def NATIONALITY(self) -> Nation:
        """Should be either one of `Mondstadt`, `Liyue`, `Inazuma`, `Sumeru`, `Monster`, `Fatui`, `Hilichurl`
        应当为`蒙德`,`璃月`,`稻妻`,`须弥`,`魔物`,`愚人众`,`丘丘人`中的一个"""
        ...

    @property
    @abstractmethod
    def WEAPON_TYPE(self) -> WeaponType:
        """Should be either one of `bow`, `claymore`, `sword`, `polearm`, `catalyst`
        应当为`弓`,`双手剑`,`单手剑`,`长柄武器`,`法器`中的一个"""
        ...

    @property
    @abstractmethod
    def health_point(self) -> int:
        ...

    @property
    @abstractmethod
    def SKILL_NUM(self) -> int:
        ...

    @property
    @abstractmethod
    def skills(self) -> list['Skill']:
        ...

    @property
    @abstractmethod
    def SKILL_NAMES(self) -> list[str]:
        ...


class Skill(ABCMeta):
    def __init__(self, name: str, cost: dict[ElementType,int], skill_type: SkillType):
        """
        Args:
        cost(dict[ElementType, int]): {ElementType:cost}; `None` if no cost is required (Please do not use empty dictionary!)
        skill_type(bool): passive skill which can only be triggered
        """
        self.NAME = name
        self.RAW_COST = cost
        self.TYPE = skill_type
        self.current_cost = cost

    @property
    @abstractmethod
    def requirements(self):
        """Description of the requirement of the skill in domain-specific language (dsl)."""
        ...

    @property
    @abstractmethod
    def targets(self):
        """Description of the target of the skill in domain-specific language (dsl).
        Use a list to assign multiple targets.
        """
        ...

    @property
    @abstractmethod
    def effects(self):
        """Description of the target of the skill in domain-specific language (dsl).
        Use a list to assign multiple effects to the targets respectively."""
        ...

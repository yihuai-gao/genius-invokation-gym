from enum import Enum
from logging import getLogger


class GameStatus(Enum):
    INITIALIZING = 0
    RUNNING = 1
    ENDED = 2


class InitializingPhase(Enum):
    CHANGE_CARD = 0
    SELECT_ACTIVE_CHARACTER = 1


class RunningPhase(Enum):
    BEGIN_ROUND = 0  # Including drawing cards automatically
    ROLL_DICE = 1
    PLAY_CARDS = 2
    END_ROUND = 3


class ET(Enum):
    '''Element types (including power, arbitrary, omni)'''
    POWER = -3
    '''元素能量'''
    SAME = -2
    '''Same Element, only used in card cost description\n
    相同元素，仅用于卡牌描述
    '''
    UNALIGNED = -1
    '''Unaligned Element, only used in skill/card cost description\n
    任意元素，仅用于角色技能/卡牌描述'''
    OMNI = 0
    '''Omni Element, only used in dice\n
    万能元素骰，仅用于骰子'''
    CRYO = 1
    '''冰'''
    HYDRO = 2
    '''水'''
    PYRO = 3
    '''火'''
    ELECTRO = 4
    '''雷'''
    GEO = 5
    '''岩'''
    DENDRO = 6
    '''草'''
    ANEMO = 7
    '''风'''


class WT(Enum):
    '''Weapon types'''
    BOW = 1
    '''弓'''
    SWORD = 2
    '''单手剑'''
    CLAYMORE = 3
    '''双手剑'''
    POLEARM = 4
    '''长柄武器'''
    CATALYST = 5
    '''法器'''


class Nation(Enum):
    Mondstadt = 1
    '''蒙德'''
    Liyue = 2
    '''璃月'''
    Inazuma = 3
    '''稻妻'''
    Sumeru = 4
    '''须弥'''
    Monster = 5
    '''魔物'''
    Fatui = 6
    '''愚人众'''
    Hilichurl = 7
    '''丘丘人'''


class ST(Enum):
    '''Skill types'''
    NORMAL_ATTACK = 1
    '''普通攻击'''
    ELEMENTAL_SKILL = 2
    '''元素技能'''
    ELEMENTAL_BURST = 3
    '''元素爆发'''
    PASSIVE_SKILL = 4
    '''被动技能'''


class Position(Enum):
    '''Character position'''
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

    def __add__(self, num: int):
        '''Modular addition for `next-character` calculation'''
        return Position((self.value+num) % 3)


class PlayerID(Enum):
    SPECTATOR = 0
    PLAYER1 = 1
    PLAYER2 = 2

    def __invert__(self):
        '''Use ~player_id to get his opponent'''
        if self.value == 1:
            return PlayerID.PLAYER2
        if self.value == 2:
            return PlayerID.PLAYER1
        logger = getLogger("gisim")
        logger.warning("You are taking the opponent of the spectator!")
        return self

from enum import Enum, IntEnum, auto
from logging import getLogger


class GameStatus(Enum):
    INITIALIZING = 0
    RUNNING = 1
    ENDED = 2


class GamePhase(Enum):
    CHANGE_CARD = 0
    """Only happens during initialization"""
    SELECT_ACTIVE_CHARACTER = 1
    """Happens during initialization or when a character die"""
    ROUND_BEGIN = 2
    """Including drawing cards automatically"""
    ROLL_DICE = 3
    PLAY_CARDS = 4
    """Or use character skills"""
    ROUND_END = 5


class ElementType(IntEnum):
    """Element types (including power, any, omni)"""

    NONE = -10
    """No element infusion/attachment; also used in normal attack"""
    POWER = -3
    """元素能量"""
    SAME = -2
    """Same Element, only used in card cost description\n
    相同元素，仅用于卡牌描述
    """
    ANY = -1
    """Any Element, only used in skill/card cost description\n
    任意元素，仅用于角色技能/卡牌描述"""
    OMNI = 0
    """Omni Element, only used in dice\n
    万能元素骰，仅用于骰子"""
    CRYO = 1
    """冰"""
    HYDRO = 2
    """水"""
    PYRO = 3
    """火"""
    ELECTRO = 4
    """雷"""
    GEO = 5
    """岩"""
    DENDRO = 6
    """草"""
    ANEMO = 7
    """风"""
    PIERCE = 10
    """穿透伤害"""

    @staticmethod
    def get_basic_elements() -> set["ElementType"]:
        """七种基础元素"""
        return {
            ElementType.CRYO,
            ElementType.HYDRO,
            ElementType.PYRO,
            ElementType.ELECTRO,
            ElementType.GEO,
            ElementType.DENDRO,
            ElementType.ANEMO,
        }


class WeaponType(Enum):
    """Weapon types"""

    BOW = 1
    """弓"""
    SWORD = 2
    """单手剑"""
    CLAYMORE = 3
    """双手剑"""
    POLEARM = 4
    """长柄武器"""
    CATALYST = 5
    """法器"""
    OTHER_WEAPONS = 6
    """其他武器"""


class Nation(Enum):
    Mondstadt = 1
    """蒙德"""
    Liyue = 2
    """璃月"""
    Inazuma = 3
    """稻妻"""
    Sumeru = 4
    """须弥"""
    Monster = 5
    """魔物"""
    Fatui = 6
    """愚人众"""
    Hilichurl = 7
    """丘丘人"""


class SkillType(Enum):
    """Skill types"""

    NORMAL_ATTACK = 1
    """普通攻击"""
    ELEMENTAL_SKILL = 2
    """元素技能"""
    ELEMENTAL_BURST = 3
    """元素爆发"""
    PASSIVE_SKILL = 4
    """被动技能"""


class CharacterPosition(Enum):
    """Character position"""

    BACKGROUND_CHARACTER = -2
    ACTIVE_CHARACTER = -1
    NONE = None
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

    def __add__(self, num: int):
        """Modular addition for `next-character` calculation"""
        assert self.value is not None
        return CharacterPosition((self.value + num) % 3)


class PlayerID(Enum):
    SPECTATOR = 0
    PLAYER1 = 1
    PLAYER2 = 2

    def __invert__(self):
        """Use ~player_id to get his opponent"""
        if self.value == 1:
            return PlayerID.PLAYER2
        if self.value == 2:
            return PlayerID.PLAYER1
        logger = getLogger("gisim")
        logger.warning("You are taking the opponent of the spectator!")
        return self


class MsgPriority(IntEnum):
    """Higher priority is with lower value (appears earlier in this Enum)
    Usually there is at most one message for each class in the message queue."""

    IMMEDIATE_OPERATION = auto()
    """ChangeCard, ChangeDice, PayCardCost, PaySkillCost, PayChangingCharacterCost\n
    Generate, prolong or remove entities, including Summon, Support, CharacterStatus, CombatStatus, Equipment, etc."""
    PLAYER_ACTION = auto()
    """UseCard, UseSkill, ChangeCharacter"""
    CHARACTER_DIED = auto()
    """Will trigger player to change their card or game end"""
    HP_CHANGED = auto()
    """Hurt, Recovered"""
    GENERAL_EFFECT = auto()
    """Including DealDamage, RecoverHp, AttachElement\n
    This message will go through a lot of region"""
    ELEMENTAL_REACTION_EFFECT = auto()
    """Including Frozen, Overloaded, Swirl, Crystalize, Quicken, Burning, Bloom, Crystallize
    Note that some reactions only modifies the damage but not generate additional effect."""
    ACTION_DONE = auto()
    """AfterUsingSkill, AfterUsingCard, AfterChangingCharacter"""
    GAME_STATUS = auto()
    """RoundStart, RoundEnd"""


class CardType(Enum):
    ARTIFACT = auto()
    TALENT = auto()
    WEAPON = auto()
    ELEMENTAL_RESONANCE = auto()
    FOOD = auto()
    NORMAL_EVENT = auto()
    ANY = auto()


class RegionType(Enum):
    CHARACTER_ZONE = auto()
    ACTIVE_CHARACTER = auto()
    SUPPORT_ZONE = auto()
    SUMMON_ZONE = auto()
    HAND = auto()
    DECK = auto()
    COMBAT_STATUS_ZONE = auto()
    DICE_ZONE = auto()
    GAME_FSM = auto()

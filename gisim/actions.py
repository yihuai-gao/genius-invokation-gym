''' Interface between the game environment and players(agents)

Start Game: SelectActiveCharacter (Also happens when the active character falls), ChangeCards

In each round: RerollDice (also happens after using some cards, e.g. 乾坤一掷)
    Combat Action: UseSkill, SelectActiveCharacter, DeclareEnd
    Fast Action: PlayCard, ElementalTuning

'''

from .entity import Entity
from abc import ABCMeta, abstractmethod
class Action(Entity, ABCMeta):
    def __init__(self, type:str):
        self._type = type
    
    def _check_cards_index(self, cards_idx:list[int]):
        assert type(cards_idx) == list
        for card in cards_idx:
            assert type(card) == int and card >= 0
    def _check_dice_index(self, dice_idx):
        assert type(dice_idx) == list
        for die_idx in dice_idx:
            assert type(die_idx) == int and die_idx >= 0  
        
class SelectActiveCharacter(Action):
    def __init__(self, position:int):
        super().__init__("SelectActiveCharacter")
        assert position in [0, 1, 2], "Position of the active character should be 0, 1, 2"
        self.position = position
        
class ChangeCards(Action):
    def __init__(self, cards_idx:list[int]):
        super().__init__("ChangeCards")
        self._check_cards_index(cards_idx)
        self.cards_idx = cards_idx
    
class RerollDice(Action):
    def __init__(self, dice_idx:list[int]):
        super().__init__("RerollDice")
        self._check_dice_index(dice_idx)
        self.dice_idx = dice_idx
            
class UseSkill(Action):
    def __init__(self, position:int, skill_name:str, dice_idx:list[int], skill_target):
        super().__init__("UseSkill")
        assert type(skill_name) == str
        assert position in [0, 1, 2], "Position of the user character should be 0, 1, 2"
        self.skill_name = skill_name
        self._check_dice_index(dice_idx)
        self.dice_idx = dice_idx
        self.skill_target = skill_target
        # TODO: Define the protocol of the skill_target: should be able to cover all characters, attachments, status, summons, supports, etc.
class DeclareEnd(Action):
    def __init__(self):
        super().__init__("DeclareEnd")

class PlayCard(Action):
    def __init__(self, card_idx:int, dice_idx:list[int], card_target):
        super().__init__("PlayCard")
        assert type(card_idx) == int and card_idx >= 0
        self.card_idx = card_idx
        self._check_dice_index(dice_idx)
        self.dice_idx = dice_idx
        self.card_target = card_target
        
        
class ElementalTuning(Action):
    def __init__(self, card_idx:int, die_idx:int):
        super().__init__("ElementalTuning")
        assert type(card_idx) == int and card_idx >= 0
        assert type(die_idx) == int and die_idx >= 0
        self.card_idx = card_idx
        self.die_idx = die_idx

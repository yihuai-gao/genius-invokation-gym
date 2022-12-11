'''Player area of the Genius Invokation
Note that player agents does not directly talk to this area, but through the judger who judges the validity of each move. The judger then publish events and then the entities in the each player area respond to it in a specific order.
'''

from .cards.card import Card
from random import random
       
class PlayerArea:
    def __init__(self, deck:dict):
        self._deck = Deck(deck['cards'])
        self._hand = Hand()
        self._element_zone = ElementZone()
        self._character_zone = CharacterZone(deck['characters'])
        self._summon_zone = SummonZone()
        self._support_zone = SupportZone()
        
        
        
class Hand:
    def __init__(self):
        self.cards = []
        
class CharacterZone:
    def __init__(self, characters:list[str]):
        assert len(characters)==3, "Number of characters should be 3"
        self.characters = [Card('character', characters[k]) for k in range(3)]


class SummonZone:
    def __init__(self):
        self.summons = []
        

class SupportZone:
    def __init__(self):
        self.supports = []
        
class ElementZone:
    def __init__(self):
        self.elements = []

class Deck:
    def __init__(self, cards:list[str]):
        self.cards = cards
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def draw_cards(self, n):
        assert n <= len(self.cards), "Card number to be drawn exceeds the deck size"
        output = self.cards[:n]
        self.cards = self.cards[n:]
        return output
'''Genius Invokation Game class
'''

import random
from .player_area import PlayerArea
class Game:
    def __init__(self, player1_deck:dict, player2_deck:dict, seed:int=50):
        self.status = 'initialized'
        self.seed = seed
        random.seed(seed)
        self.player1_area = PlayerArea(player1_deck)
        self.player2_area = PlayerArea(player2_deck)
        

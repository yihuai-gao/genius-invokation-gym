import logging

from gisim.agent import AttackOnlyAgent, NoAttackAgent
from gisim.game import Game
from gisim.run import run_game

logging.basicConfig(level=logging.INFO, format="%(message)s")
if __name__ == "__main__":
    player1_deck = {
        "characters": ["Kamisato Ayaka", "Kamisato Ayaka", "Kamisato Ayaka"],
        "cards": ["Kanten Senmyou Blessing", "Sacrificial Sword"],
    }
    player2_deck = {
        "characters": ["Kamisato Ayaka", "Kamisato Ayaka", "Kamisato Ayaka"],
        "cards": [],
    }

    game = Game()
    game.init_deck(player1_deck, player2_deck, seed=10)
    run_game(game, AttackOnlyAgent, NoAttackAgent)

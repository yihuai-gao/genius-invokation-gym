import logging

from gisim.agent import AttackOnlyAgent, NoAttackAgent
from gisim.game import Game
from gisim.run import run_game

logging.basicConfig(level=logging.INFO, format="%(message)s")
if __name__ == "__main__":

    player1_deck = {
        "characters": ["RaidenShogun", "Xingqiu", "Sucrose"],
        "cards": ["Sacrificial Sword"],
    }
    player2_deck = {
        "characters": ["KamisatoAyaka", "Xingqiu", "Sucrose"],
        "cards": [],
    }

    game = Game()
    game.init_deck(player1_deck, player2_deck, seed=10)
    run_game(game, AttackOnlyAgent, AttackOnlyAgent)

from gisim import Game, Agent, Judge
from gisim.classes.enums import PlayerID

if __name__ == "__main__":
    player1_deck = {"characters": ["宵宫", "神里绫华", "重云"], "cards":[]}
    player2_deck = {"characters": ["菲谢尔", "柯莱", "香菱"], "cards":[]}
    game = Game(player1_deck, player2_deck)

    game_end = False
    game_info = game.encode_game_info(PlayerID.SPECTATOR)


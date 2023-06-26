def get_game_info():
    from gisim.game import Game

    game = Game()
    return game.encode_game_info()


import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from gisim.agent import AttackOnlyAgent  # noqa: E402
from gisim.classes.enums import GameStatus, PlayerID  # noqa: E402
from gisim.game import Game  # noqa: E402

if __name__ == "__main__":
    # player1_deck = {"characters": ["宵宫", "神里绫华", "重云"], "cards": []}
    # player2_deck = {"characters": ["菲谢尔", "柯莱", "香菱"], "cards": []}
    player1_deck = {
        "characters": ["Yoimiya", "Kamisato Ayaka", "Chongyun"],
        "cards": [],
    }
    player2_deck = {"characters": ["Fischl", "Collei", "Xiangling"], "cards": []}
    game = Game(player1_deck, player2_deck)
    player1_agent = AttackOnlyAgent(PlayerID.PLAYER1)
    player2_agent = AttackOnlyAgent(PlayerID.PLAYER2)
    game_end = False
    game_info = game.encode_game_info(PlayerID.SPECTATOR)

    winner = PlayerID.SPECTATOR
    action_cnt = 0
    while True:
        action_cnt += 1
        print(f"Action {action_cnt}")
        active_player = game_info.active_player
        if active_player == PlayerID.PLAYER1:
            action = player1_agent.take_action(game_info)
        else:
            action = player2_agent.take_action(game_info)
        valid = game.judge.judge_action(active_player, action)
        if valid:
            game.step(action)
            game_info = game.encode_game_info()
            if game_info.status == GameStatus.ENDED:
                winner = game.get_winner()
                break
        else:
            print(f"The action of {active_player} is invalid. Game End.")
            winner = ~active_player
            break

    if winner is PlayerID.SPECTATOR:
        print(f"The game is a draw")
    else:
        print(f"The winner is {winner}")

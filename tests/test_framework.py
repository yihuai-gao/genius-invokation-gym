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
    game = Game(player1_deck, player2_deck, seed=10)
    player1_agent = AttackOnlyAgent(PlayerID.PLAYER1)
    player2_agent = AttackOnlyAgent(PlayerID.PLAYER2)
    game_end = False
    game_info = game.encode_game_info(PlayerID.SPECTATOR)

    winner = PlayerID.SPECTATOR
    action_cnt = 0
    while True:
        action_cnt += 1
        active_player = game_info.active_player
        if active_player == PlayerID.PLAYER1:
            action = player1_agent.take_action(game_info)
        else:
            action = player2_agent.take_action(game_info)
        print(f"\nGame round {game_info.round_num} phase {game_info.phase}")
        if active_player == PlayerID.PLAYER1:
            if game_info.player1.dice_zone:
                dice = [str(die) for die in game_info.player1.dice_zone]
            else:
                dice = []
        else:
            if game_info.player2.dice_zone:
                dice = [str(die) for die in game_info.player2.dice_zone]
            else:
                dice = []
        print(f"  {active_player} Dice: {dice}")
        print(f"      {str(type(action)).strip().split('.')[-1]}: {action.dict()}")
        valid = game.judge_action(action)
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
        if action_cnt >= 100:
            break

    if winner is PlayerID.SPECTATOR:
        print(f"The game is a draw")
    else:
        print(f"The winner is {winner}")

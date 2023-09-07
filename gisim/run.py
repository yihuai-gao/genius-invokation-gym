import logging
from typing import TYPE_CHECKING, Type

from hbutils.string import ordinalize
from player_area import PlayerInfo

from gisim.agent import Agent
from gisim.classes.enums import CharPos, GameStatus, PlayerID, Winner

if TYPE_CHECKING:
    from gisim.game import Game


def print_player_info(player_info: PlayerInfo):

    if player_info.dice_zone:
        dice = [str(die) for die in player_info.dice_zone]
    else:
        dice = []
    ch = None
    ch_status_list = []
    weapon = {}
    talent = {}
    artifact = {}
    cards = player_info.hand_cards
    pos = player_info.active_character_position
    combat_status_list = []
    if pos is not CharPos.NONE:
        ch = player_info.characters[pos.value].character
        ch_status_list = player_info.characters[pos.value].status
        weapon = player_info.characters[pos.value].weapon
        talent = player_info.characters[pos.value].talent
        artifact = player_info.characters[pos.value].artifact
        combat_status_list = player_info.combat_status_zone
    summons = player_info.summon_zone

    logging.info(f"{player_info.player_id}")
    logging.info(f"    Current Dice: {dice}")
    if cards:
        logging.info(f"    Current Cards: {cards}")
    if ch is not None:
        logging.info(
            f"    Current Character: {ch.name}, hp: {ch.health_point}, power: {ch.power}/{ch.max_power}, elem attachment: {ch.elemental_attachment}"
        )
    if weapon:
        logging.info(
            f"        Weapon: {weapon['name']}, active: {weapon['active']}, triggered times: {weapon['triggered_in_a_round']}"
        )
    if talent:
        logging.info(
            f"        Talent: {talent['name']}, active: {talent['active']}, triggered times: {talent['triggered_in_a_round']}"
        )
    if artifact:
        logging.info(
            f"        Artifact: {artifact['name']}, active: {artifact['active']}, triggered times: {artifact['triggered_in_a_round']}"
        )
    if len(ch_status_list) >= 1:
        logging.info(f"        Character Status:")
        for status in ch_status_list:
            logging.info(
                f"            {status['name']}, active: {status['active']}, remaining round: {status['remaining_round']}, remaining usage: {status['remaining_usage']}"
            )
    if summons:
        logging.info(f"    Current Summons:")
        for summon in summons:
            logging.info(f"          {summon['name']}: usages: {summon['usages']}")

    if len(combat_status_list) >= 1:
        logging.info(f"    Combat Status:")
        for combat_status in combat_status_list:
            logging.info(
                f"      {combat_status['player_id']},{combat_status['name']}, active: {combat_status['active']}, remaining round: {combat_status['remaining_round']}, remaining usage: {combat_status['remaining_usage']}"
            )


def run_game(
    game: "Game",
    player1_agent_cls: Type[Agent],
    player2_agent_cls: Type[Agent],
    max_action_count: int = 100,
):
    logging.info(f"Game initializing: {game!r}")

    player1_agent = player1_agent_cls(PlayerID.PLAYER1)
    player2_agent = player2_agent_cls(PlayerID.PLAYER2)
    logging.info(f"Player 1: {player1_agent!r}")
    logging.info(f"Player 2: {player2_agent!r}")

    game_info = game.encode_game_info(PlayerID.SPECTATOR)

    winner = Winner.UNFINISHED
    action_cnt = 0
    game_round = 0
    while True:
        if game_round != game_info.round_num:
            game_round = game_info.round_num
            logging.info(
                f"-------------- {ordinalize(game_round)} Round --------------"
            )

        action_cnt += 1
        active_player = game_info.active_player

        if active_player == PlayerID.PLAYER1:
            action = player1_agent.take_action(game_info)
        else:
            action = player2_agent.take_action(game_info)

        print_player_info(game_info.player1)
        print_player_info(game_info.player2)
        logging.info(
            f"\n{active_player} {action.__class__.__name__}: {action.dict()}\n"
        )

        valid = game.judge_action(action)
        if valid:
            game.step(action)
            game_info = game.encode_game_info()
            if game_info.status == GameStatus.ENDED:
                winner = game_info.winner
                break
        else:
            logging.error(f"The action of {active_player!r} is invalid. Game End.")
            winner = Winner((~active_player).value)
            break

        if action_cnt >= max_action_count:
            logging.warning(
                f"Max action count ({max_action_count}) exceeded, quit the game."
            )
            break

    if winner is Winner.DRAW:
        logging.info(f"The game is a draw.")
    else:
        logging.info(f"The winner is {winner}")

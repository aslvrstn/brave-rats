import argparse
import sys
from collections import Counter

from brains.Brain import Brain
from brains.example_ai import RandomAI
from brains.human import HumanBrain
from components.cards import Color
from components.fight import resolve_fight, successful_spy_color
from components.game_status import GameStatus
from components.player import Player
from components.style import blueify, redify


def _get_played_cards(red_player, blue_player, game):
    spy_color = successful_spy_color(game.most_recent_fight)
    if spy_color == Color.red:
        # Red gets to peek at Blue's card
        blue_card = blue_player.choose_and_play_card(game)
        red_card = red_player.choose_and_play_card(game, blue_card)
    elif spy_color == Color.blue:
        # Blue gets to peek at Red's card
        red_card = red_player.choose_and_play_card(game)
        blue_card = blue_player.choose_and_play_card(game, red_card)
    else:
        red_card, blue_card = red_player.choose_and_play_card(
            game
        ), blue_player.choose_and_play_card(game)
    return red_card, blue_card


def play_game(
    red_brain: Brain = None,
    blue_brain: Brain = None,
    initial_red_hand_str=None,
    initial_blue_hand_str=None,
    verbose=True,
):
    if red_brain is None:
        red_brain = HumanBrain()
    if blue_brain is None:
        blue_brain = RandomAI()

    game = GameStatus()
    red_player = Player(Color.red, brain=red_brain, hand_str=initial_red_hand_str)
    blue_player = Player(Color.blue, brain=blue_brain, hand_str=initial_blue_hand_str)

    while not game.is_over:
        red_card, blue_card = _get_played_cards(red_player, blue_player, game)
        result = resolve_fight(red_card, blue_card, game)
        if verbose:
            result_string = "red {} vs. blue {} -> {}"
            print(
                result_string.format(
                    redify(red_card.name), blueify(blue_card.name), result.name
                )
            )
            print(game.score_summary)

    if verbose:
        if game.winner:
            print(game.winner.name.title(), "wins!")
        else:
            print("tie!")
        print()  # extra newline for readability

    return game


def print_match_summary(games):
    winners = [game.winner for game in games]
    print("Total wins for each player:")
    win_counter = Counter(winners)
    for player, wins in win_counter.items():
        if player is None:
            print("{} ties".format(wins))
        else:
            print("{} won {} times".format(player.name, wins))


def play_match(
    red_brain=None, blue_brain=None, num_games=1, verbose=True, quiet_games=True
):
    if red_brain is None:
        red_brain = HumanBrain()
    if blue_brain is None:
        blue_brain = RandomAI()

    if verbose:
        sys.stdout.write("\n")
    for game_index in range(num_games):
        game = play_game(
            red_brain=red_brain, blue_brain=blue_brain, verbose=not quiet_games
        )
        if quiet_games and verbose:
            # Games are quiet, so print some stuff at this level
            winner_summary_lookup = {
                Color.red: redify("r"),
                Color.blue: blueify("b"),
                None: "t",
            }
            sys.stdout.write(winner_summary_lookup[game.winner])
        yield game

    if verbose:
        sys.stdout.write("\n")


def args_from_match_parser():
    """Fire up an argparser designed to kick off a Brave Rats match between two AIs
    :return: dict of parsed args suitable for passing to play_match()
    """

    parser = argparse.ArgumentParser(description="Play a match of Brave Rats games")
    parser.add_argument(
        "-r", "--red-brain", help="Brain function name to use for red player"
    )
    parser.add_argument(
        "-b", "--blue-brain", help="Brain function name to use for blue player"
    )
    parser.add_argument(
        "-n", "--num-games", type=int, help="Number of games to play in this match"
    )
    parser.add_argument(
        "-q",
        "--quiet-games",
        action="store_true",
        default=False,
        help="Set to have only game results (not turn-by-turn details) printed to stdout",
    )
    args = vars(parser.parse_args())  # Convert the Namespace to a dict
    args = {k: v for k, v in list(args.items()) if v is not None}  # Remove None values

    # Look up brains by name
    class_by_name = {
        "random": RandomAI,
        "human": HumanBrain,
    }
    if "red_brain" in args:
        args["red_brain_fn"] = class_by_name[args.pop("red_brain")]()
    if "blue_brain" in args:
        args["blue_brain_fn"] = class_by_name[args.pop("blue_brain")]()
    return args


if __name__ == "__main__":
    games = play_match(**args_from_match_parser())
    print_match_summary(games)

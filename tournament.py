#!/usr/bin/python
#  -*- coding: UTF8 -*-
import argparse
import sys
from collections import Counter

from brains.beat_opponent_random import BeatOpponentRandomAI
from brains.example_ai import RandomAI
from brains.random_plus_beat_spied import RandomPlusBeatSpiedAI
from brave_rats import play_match
from components.cards import Color
from components.style import blueify, color_pad, redify

EXCLUDED_BRAIN_NAMES = {"human"}


def _table_cell(contents):
    return " {:22} |".format(contents)


def _print_table_cell(contents):
    sys.stdout.write(_table_cell(contents))


def _print_table_row(contents):
    for item in contents:
        _print_table_cell(item)
    sys.stdout.write("\n")


def _print_summary(results, ai_names):
    _print_table_row(["*"] + [blueify(name) for name in ai_names])
    for red_ai in ai_names:
        _print_table_cell(redify(red_ai))
        for blue_ai in ai_names:
            try:
                games = results[(red_ai, blue_ai)]
            except KeyError:
                win_count = {Color.red: "-", Color.blue: "-", None: "-"}
            else:
                winners = [game.winner for game in games]
                win_count = Counter(winners)
            result_descrip = "{}/{}/{}".format(
                "←{}".format(win_count[Color.red]),
                win_count[None],
                "↑{}".format(win_count[Color.blue]),
            )
            if win_count[Color.red] > win_count[Color.blue]:
                colored_result_descrip = redify(result_descrip)
            elif win_count[Color.red] < win_count[Color.blue]:
                colored_result_descrip = blueify(result_descrip)
            else:
                colored_result_descrip = color_pad(result_descrip)
            _print_table_cell(colored_result_descrip)
        _print_table_row([])


def play_round_robin(num_games=1000, interactive=False):
    # New AIs need to go into this dict
    brains_dict = {"random": RandomAI,
                   "randomPlusBeatSpied": RandomPlusBeatSpiedAI,
                   "beatOpponentRandom": BeatOpponentRandomAI
                   }

    ai_names = brains_dict.keys()

    print("{} AIs discovered:".format(len(ai_names)))
    print("AIs:")
    print("\n".join(ai_names))

    results = {}
    for red_ai_name, red_ai_class in brains_dict.items():
        for blue_ai_name, blue_ai_class in brains_dict.items():
            next_match_intro = "Next match: {} vs. {}".format(
                redify(red_ai_name), blueify(blue_ai_name)
            )
            if interactive:
                input(next_match_intro)
            else:
                print(next_match_intro)

            games = list(
                play_match(
                    red_ai_class(),
                    blue_ai_class(),
                    num_games=num_games,
                    verbose=True,
                    quiet_games=True,
                )
            )
            results[(red_ai_name, blue_ai_name)] = games
            _print_summary(results, ai_names)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Play a tournament of Brave Rats matches"
    )
    parser.add_argument(
        "-n",
        "--num-games",
        type=int,
        default=1000,
        help="Number of games to play in each match",
    )
    parser.add_argument(
        "-i", "--interactive", default=False, action="store_true", help="Requires"
    )
    args = parser.parse_args()

    play_round_robin(num_games=args.num_games, interactive=args.interactive)

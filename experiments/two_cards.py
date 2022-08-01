import itertools
from typing import List, Dict

from components.cards import Card
from components.fight import QUICK_FIGHT_RESULT
from components.game_status import GameStatus

ALL_CARDS = [card for card in Card]


def play_a_round(red_hand: List[Card], blue_hand: List[Card], game: GameStatus):
    if not red_hand or not blue_hand:
        return

    max_by_play: Dict[Card, int] = {}
    min_by_play: Dict[Card, int] = {}

    all_results = []
    for red_plays in red_hand:
        this_play_results = []
        for blue_plays in blue_hand:
            new_red_hand = red_hand.copy()
            new_blue_hand = blue_hand.copy()
            new_red_hand.remove(red_plays)
            new_blue_hand.remove(blue_plays)
            new_game = game.clone()
            new_game.resolve_fight(red_plays, blue_plays)
            all_results.append(new_game)
            this_play_results.append(new_game)
            play_a_round(new_red_hand, new_blue_hand, new_game)
        max_by_play[red_plays] = max([res.red_points for res in this_play_results])
        min_by_play[red_plays] = min([res.red_points for res in this_play_results])

    print("********")
    print(max([res.red_points for res in all_results]))
    print(min([res.red_points for res in all_results]))
    print(max_by_play)
    print(min_by_play)
    for c1 in red_hand:
        for c2 in red_hand:
            if c1 == c2:
                continue
            if min_by_play[c1] >= max_by_play[c2]:
                print(f"{c1} dominates {c2}")
    for res in all_results:
        print(res.blue_points, res.red_points, res.winner, res.resolved_fights)


def foo():
    all_hands = list(itertools.combinations(ALL_CARDS, 4))
    for red_hand_t in all_hands:
        for blue_hand_t in all_hands:
            play_a_round(list(red_hand_t), list(blue_hand_t), GameStatus())


if __name__ == "__main__":
    foo()
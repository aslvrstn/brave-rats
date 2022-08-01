import itertools
from typing import List, Dict

from components.cards import Card, Color
from components.game_status import GameStatus

ALL_CARDS = [card for card in Card]


def play_a_round(red_hand: List[Card], blue_hand: List[Card], game: GameStatus) -> Color:
    if game.winner:
        return 1.0 if game.winner == Color.red else 0.0
    if not red_hand or not blue_hand:
        return 0.5

    avg_by_red_card: Dict[Card, float] = {}

    all_results = []
    for red_plays in red_hand:
        this_play_results = []
        tot_score = 0.0
        for blue_plays in blue_hand:
            new_red_hand = red_hand.copy()
            new_blue_hand = blue_hand.copy()
            new_red_hand.remove(red_plays)
            new_blue_hand.remove(blue_plays)
            new_game = game.clone()
            new_game.resolve_fight(red_plays, blue_plays)
            all_results.append(new_game)
            this_play_results.append(new_game)
            tot_score += play_a_round(new_red_hand, new_blue_hand, new_game)
        avg_score = tot_score / len(blue_hand)
        avg_by_red_card[red_plays] = avg_score

    print("********")
    print(avg_by_red_card)
    for res in all_results:
        print(res.blue_points, res.red_points, res.winner, res.resolved_fights)

    return max(avg_by_red_card.values())


def foo():
    all_hands = list(itertools.combinations(ALL_CARDS, 3))
    for red_hand_t in all_hands:
        for blue_hand_t in all_hands:
            play_a_round(list(red_hand_t), list(blue_hand_t), GameStatus())


if __name__ == "__main__":
    foo()
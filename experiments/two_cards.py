import itertools
from typing import List, Dict, Tuple

from components.cards import Card, Color
from components.game_status import GameStatus, POINTS_TO_WIN

ALL_CARDS = [card for card in Card]


def play_a_round(red_hand: List[Card], blue_hand: List[Card], game: GameStatus) -> Tuple[float, List[Card]]:
    if game.winner:
        return (1.0, []) if game.winner == Color.red else (0.0, [])
    if not red_hand or not blue_hand:
        return (0.5, [])

    avg_by_red_card: Dict[Card, float] = {}

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
            this_play_results.append(new_game)
            val, played_from_here = play_a_round(new_red_hand, new_blue_hand, new_game)
            tot_score += val
        avg_score = tot_score / len(blue_hand)
        avg_by_red_card[red_plays] = avg_score

    best_card = None
    best_val = 0.0
    for card, val in avg_by_red_card.items():
        if val >= best_val:
            best_card = card
            best_val = val
    return best_val, [best_card]


def foo():
    # Start off with some points (assuming the game is split, basically), so that this is interesting playing only
    # a few rounds.
    cards_to_play = 4
    starting_points = (7 - cards_to_play) // 2

    initial_game_state = GameStatus(red_points=starting_points, blue_points=starting_points)
    all_hands = list(itertools.combinations(ALL_CARDS, cards_to_play))
    for red_hand_t in all_hands:
        for blue_hand_t in all_hands:
            score, played = play_a_round(list(red_hand_t), list(blue_hand_t), initial_game_state)
            # Find hands that are really good for red
            if score >= 0.9:
                print(f"{red_hand_t} vs {blue_hand_t}: {score} {played}")


if __name__ == "__main__":
    foo()
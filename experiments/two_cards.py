import itertools
from dataclasses import dataclass
from typing import List, Dict, Tuple, FrozenSet, Optional

from components.cards import Card, Color
from components.game_status import GameStatus

ALL_CARDS = [card for card in Card]


@dataclass(frozen=True)
class MemoizableState:
    red_hand: FrozenSet[Card]
    blue_hand: FrozenSet[Card]
    red_points: int
    blue_points: int
    on_hold_fights: Tuple[Tuple]


cached_res: Dict[MemoizableState, Tuple] = {}


def play_a_round(red_hand: List[Card], blue_hand: List[Card], game: GameStatus) -> Tuple[float, Optional[Card]]:
    ms = MemoizableState(frozenset(red_hand), frozenset(blue_hand), game.red_points, game.blue_points, tuple(game.on_hold_fights))
    if ms in cached_res:
        return cached_res[ms]
    if game.winner:
        return (1.0, None) if game.winner == Color.red else (0.0, None)
    if not red_hand or not blue_hand:
        return (0.5, None)

    min_by_red_card: Dict[Card, float] = {}

    for red_plays in red_hand:
        this_play_results = []
        scores = []
        for blue_plays in blue_hand:
            new_red_hand = red_hand.copy()
            new_blue_hand = blue_hand.copy()
            new_red_hand.remove(red_plays)
            new_blue_hand.remove(blue_plays)
            new_game = game.clone()
            new_game.resolve_fight(red_plays, blue_plays)
            this_play_results.append(new_game)
            val, played_from_here = play_a_round(new_red_hand, new_blue_hand, new_game)
            scores.append(val)
        min_by_red_card[red_plays] = min(scores)

    best_card = None
    best_val = 0.0
    for card, val in min_by_red_card.items():
        if val >= best_val:
            best_card = card
            best_val = val
    cached_res[ms] = (best_val, best_card)
    return best_val, best_card


def play_it_forward(game: GameStatus, red_hand: List[Card], blue_hand: List[Card], depth: int=0) -> None:
    def indent_string(depth: int):
        if depth == 0:
            return ""
        return "|" + "-" * 3 * depth + ">" if depth else ""

    # Play the game forward to try to build up a plausible game tree
    if game.winner:
        print(f"{indent_string(depth+1)}{game.winner.name} wins!")
        return
    elif not red_hand:
        print(blue_hand)
        print(f"{indent_string(depth+1)}Tie!")
        return

    _, red_plays = play_a_round(red_hand, blue_hand, game)
    print(f"{indent_string(depth)}Red plays: {red_plays.name}")
    for blue_plays in blue_hand:
        print(f"{indent_string(depth+1)}If blue plays {blue_plays.name}:")
        red_copy = red_hand.copy()
        blue_copy = blue_hand.copy()
        red_copy.remove(red_plays)
        blue_copy.remove(blue_plays)
        game_copy = game.clone()
        game_copy.resolve_fight(red_plays, blue_plays)
        play_it_forward(game_copy, red_copy, blue_copy, depth=depth+1)


def foo():
    # Start off with some points (assuming the game is split, basically), so that this is interesting playing only
    # a few rounds.
    cards_to_play = 4
    starting_points = (len(ALL_CARDS) - cards_to_play) // 2

    initial_game_state = GameStatus(red_points=starting_points, blue_points=starting_points)
    all_hands = list(itertools.combinations(ALL_CARDS, cards_to_play))
    for red_hand_t in all_hands:
        for blue_hand_t in all_hands:
            score, played = play_a_round(list(red_hand_t), list(blue_hand_t), initial_game_state)
            # Find hands that are really good for red
            if score >= 0.9:
                print(f"{red_hand_t} vs {blue_hand_t}: {score} {played}")

                play_it_forward(initial_game_state.clone(), list(red_hand_t), list(blue_hand_t))


if __name__ == "__main__":
    foo()
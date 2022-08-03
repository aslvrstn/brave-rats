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


def play_a_spied_round(red_hand: List[Card], blue_hand: List[Card], blue_plays: Card, game: GameStatus) -> Tuple[float, Optional[Card]]:
    assert blue_plays in blue_hand

    best_red_score = 0.0
    best_red_response = None

    for red_plays in red_hand:
        new_red_hand = red_hand.copy()
        new_blue_hand = blue_hand.copy()
        new_red_hand.remove(red_plays)
        new_blue_hand.remove(blue_plays)
        new_game = game.clone()
        new_game.resolve_fight(red_plays, blue_plays)
        val, played_from_here = play_a_round(new_red_hand, new_blue_hand, new_game)
        if val >= best_red_score:
            best_red_score = val
            best_red_response = red_plays

    return best_red_score, best_red_response


def play_a_round(red_hand: List[Card], blue_hand: List[Card], game: GameStatus) -> Tuple[float, Optional[Card]]:
    ms = MemoizableState(frozenset(red_hand), frozenset(blue_hand), game.red_points, game.blue_points, tuple(game.on_hold_fights))
    if ms in cached_res:
        return cached_res[ms]
    if game.winner:
        return (1.0, None) if game.winner == Color.red else (0.0, None)
    if not red_hand or not blue_hand:
        return (0.5, None)

    # TODO: This isn't well tested!
    if game.spy_color() == Color.red:
        best_case_for_blue = 1.0  # The worst outcome for blue
        red_responds = None
        for blue_plays in blue_hand:
            red_response_score, red_response = play_a_spied_round(red_hand, blue_hand, blue_plays, game.clone())
            if red_response_score <= best_case_for_blue:
                best_case_for_blue = red_response_score
                red_responds = red_response

        return best_case_for_blue, red_responds

    min_by_red_card: Dict[Card, float] = {}

    for red_plays in red_hand:
        scores = []
        for blue_plays in blue_hand:
            new_red_hand = red_hand.copy()
            new_blue_hand = blue_hand.copy()
            new_red_hand.remove(red_plays)
            new_blue_hand.remove(blue_plays)
            new_game = game.clone()
            new_game.resolve_fight(red_plays, blue_plays)
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

    print(f"{indent_string(depth)}{game}")
    if game.spy_color() == Color.red:
        print(f"{indent_string(depth)}Red gets to spy")
        for blue_plays in blue_hand:
            _, red_plays = play_a_spied_round(red_hand, blue_hand,blue_plays, game)
            red_copy = red_hand.copy()
            blue_copy = blue_hand.copy()
            red_copy.remove(red_plays)
            blue_copy.remove(blue_plays)
            game_copy = game.clone()
            game_copy.resolve_fight(red_plays, blue_plays)
            print(f"{indent_string(depth + 1)}If blue plays {blue_plays.name}:")
            print(f"{indent_string(depth + 1)}Red responds with: {red_plays.name}")
            play_it_forward(game_copy, red_copy, blue_copy, depth=depth + 1)
    else:
        _, red_plays = play_a_round(red_hand, blue_hand, game)
        print(f"{indent_string(depth)}Red plays: {red_plays.name}")
        for blue_plays in blue_hand:
            red_copy = red_hand.copy()
            blue_copy = blue_hand.copy()
            red_copy.remove(red_plays)
            blue_copy.remove(blue_plays)
            game_copy = game.clone()
            game_copy.resolve_fight(red_plays, blue_plays)
            print(f"{indent_string(depth + 1)}If blue plays {blue_plays.name}:")
            play_it_forward(game_copy, red_copy, blue_copy, depth=depth + 1)


def foo():
    cards_to_play = 4
    # Make it so you need to win a best-of the remaining rounds. Possibly instead want to allow splitting for evens
    points_to_win = (cards_to_play // 2) + 1
    initial_game_state = GameStatus(points_to_win=points_to_win)
    all_hands = list(itertools.combinations(ALL_CARDS, cards_to_play))
    winning_count = 0
    for red_hand_t in all_hands:
        for blue_hand_t in all_hands:
            score, played = play_a_round(list(red_hand_t), list(blue_hand_t), initial_game_state)
            # Find hands that are really good for red
            if score >= 0.9:
                winning_count += 1
                print(f"{red_hand_t} vs {blue_hand_t}: {score} {played}")
                play_it_forward(initial_game_state.clone(), list(red_hand_t), list(blue_hand_t))
    print(f"{winning_count} hands are wins")


def test_spying():
    red_hand = [Card.general, Card.princess]
    blue_hand = [Card.general, Card.prince]

    # Set it up so red gets to spy
    prev = (Card.spy, Card.princess)
    initial_game_state = GameStatus(points_to_win=2, resolved_fights=[prev])
    assert initial_game_state.spy_color() == Color.red

    score, played = play_a_round(red_hand, blue_hand, initial_game_state)
    play_it_forward(initial_game_state.clone(), red_hand, blue_hand)


if __name__ == "__main__":
    foo()
    print("** Testing spying **")
    test_spying()
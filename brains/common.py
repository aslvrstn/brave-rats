from typing import List, Tuple

from components.cards import Card
from components.fight import QUICK_FIGHT_RESULT, FightResult


# Like `best_card_against` but returns all cards that produce the same result
def best_cards_against(
    hand: List[Card], prev_round: Tuple[Card, Card], opponent_card: Card
) -> List[Card]:
    if not hand:
        raise ValueError("Hand must not be empty")

    our_previous_card, opponent_previous_card = prev_round

    # Start with the worst possible result. In this call, we are always "red"
    best_result = FightResult.blue_wins_game
    cards_that_produce_best_result = []
    # Loop over every card to find the best possible FightResult with what we have
    for card in hand:
        res = QUICK_FIGHT_RESULT[
            (card, opponent_card, our_previous_card, opponent_previous_card)
        ]

        # `FightResult` is ordered in ascending order for "red", who we are pretending to be
        # >= so that we at least always replace `best_card=None` with a real card
        if res > best_result:
            best_result = res
            cards_that_produce_best_result = [card]
        elif res == best_result:
            cards_that_produce_best_result.append(card)
    return cards_that_produce_best_result


# TODO: This should be cacheable, and is currently the slowest bit
def best_card_against(
    hand: List[Card], prev_round: Tuple[Card, Card], opponent_card: Card
) -> Card:
    # Just pick an arbitrary card
    return best_cards_against(hand, prev_round, opponent_card)[0]

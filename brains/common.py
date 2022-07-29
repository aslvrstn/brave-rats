from typing import List, Tuple

from components.cards import Card
from components.fight import QUICK_FIGHT_RESULT, FightResult


# TODO: This should be cacheable, and is currently the slowest bit
def best_card_against(
    hand: List[Card], prev_round: Tuple[Card, Card], opponent_card: Card
) -> Card:
    if not hand:
        raise ValueError("Hand must not be empty")

    our_previous_card, opponent_previous_card = prev_round

    # Start with the worst possible result. In this call, we are always "red"
    best_result = FightResult.blue_wins_game
    best_card = None
    # Loop over every card to find the best possible FightResult with what we have
    for card in hand:
        res = QUICK_FIGHT_RESULT[
            (card, opponent_card, our_previous_card, opponent_previous_card)
        ]

        # `FightResult` is ordered in ascending order for red, so compare in the right direction.
        # >= so that we at least always replace `best_card=None` with a real card
        if res >= best_result:
            best_result = res
            best_card = card
    return best_card

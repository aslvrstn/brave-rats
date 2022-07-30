import itertools
import random
from typing import Optional, Set

from brains.Brain import Brain
from brains.common import best_card_against, best_cards_against
from components.cards import Card
from components.game_status import GameStatus
from components.player import Player


class InProgressAI(Brain):
    def play_turn(
        self,
        player: Player,
        game: GameStatus,
        spied_card: Optional[Card],
        opponent_hand: Optional[Set[Card]],
    ) -> Card:
        # Only works if we get to track opponent hands
        assert opponent_hand

        # If we spied, and we have a choice, let's do something smart
        if spied_card and len(player.hand) > 1:
            return best_card_against(
                player.hand, game.recent_fight_for(player.color), spied_card
            )

        # For each opponent card, figure out all best responses, then randomly choose between them, respecting
        # duplicates across opponent cards
        best_responses_by_opp_card = {
            opp_card: best_cards_against(
                player.hand, game.recent_fight_for(player.color), opp_card
            )
            for opp_card in opponent_hand
        }
        return random.choice(
            list(itertools.chain(*best_responses_by_opp_card.values()))
        )

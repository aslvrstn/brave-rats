import itertools
import random
from typing import Optional, Set

from brains.Brain import Brain
from brains.common import best_card_against, best_cards_against
from brains.random_best_outcome import RandomBestOutcome
from brave_rats import _get_played_cards
from components.cards import Card, Color
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

        if len(player.hand) == 1:
            return player.hand[0]

        if spied_card:
            return best_card_against(
                player.hand, game.recent_fight_for(player.color), spied_card
            )

        # TODO: This block needs to come out
        loop_player = Player(player.color, RandomBestOutcome(), player.hand.copy())
        opp_color = Color.red if player.color == Color.blue else Color.blue
        loop_opp = Player(opp_color, RandomBestOutcome(), list(opponent_hand))
        cloned_game = game.clone()
        while not cloned_game.winner and loop_player.hand:
            red_player = loop_player if player.color == Color.red else loop_opp
            blue_player = loop_player if player.color == Color.blue else loop_opp
            # TODO: Handle `notify_of_hand`?
            red_card, blue_card = _get_played_cards(red_player, blue_player, cloned_game)
            cloned_game.resolve_fight(red_card, blue_card)

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

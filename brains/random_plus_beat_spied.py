import random
from typing import Optional, Set

from brains.Brain import Brain
from components.cards import Card, Color
from components.fight import QUICK_FIGHT_RESULT, FightResult
from components.game_status import GameStatus
from components.player import Player


class RandomPlusBeatSpiedAI(Brain):
    def play_turn(
        self,
        player: Player,
        game: GameStatus,
        spied_card: Optional[Card],
        opponent_hand: Optional[Set[Card]],
    ) -> Card:
        # If we spied, and we have a choice, let's do something smart
        if spied_card and len(player.hand) > 1:
            # Start with the worst possible result
            best_result = (
                FightResult.blue_wins_game
                if player.color == Color.red
                else FightResult.red_wins_game
            )
            best_card = None
            # Loop over every card to find the best possible FightResult with what we have
            for card in player.hand:
                previous_red_card, previous_blue_card = game.most_recent_fight
                red_card = card if player.color == Color.red else spied_card
                blue_card = card if player.color == Color.blue else spied_card
                res = QUICK_FIGHT_RESULT[
                    (red_card, blue_card, previous_red_card, previous_blue_card)
                ]

                # `FightResult` is ordered in ascending order for blue, so compare in the right direction.
                # >= so that we at least always replace `best_card=None` with a real card
                is_better = (
                    (res >= best_result)
                    if player.color == Color.blue
                    else (res <= best_result)
                )
                if is_better:
                    best_result = res
                    best_card = card
            return best_card
        return random.choice(player.hand)

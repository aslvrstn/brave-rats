import random
from typing import Optional, Set

from brains.Brain import Brain
from brains.common import best_card_against
from components.cards import Card
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
            return best_card_against(
                player.hand, game.recent_fight_for(player.color), spied_card
            )
        return random.choice(player.hand)

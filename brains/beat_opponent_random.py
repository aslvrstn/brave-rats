import random
from typing import Optional, Set

from brains.Brain import Brain
from brains.common import best_card_against
from components.cards import Card
from components.game_status import GameStatus
from components.player import Player


class BeatOpponentRandomAI(Brain):
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

        # Pick a random card from the opponent and pretend they will play that, then try to beat it
        opponent_plays = random.choice(list(opponent_hand))
        return best_card_against(
            player.hand, game.recent_fight_for(player.color), opponent_plays
        )

import random
from typing import Optional, Set

from brains.Brain import Brain
from components.cards import Card
from components.game_status import GameStatus
from components.player import Player


class RandomAI(Brain):
    def play_turn(
        self,
        player: Player,
        game: GameStatus,
        spied_card: Optional[Card],
        opponent_hand: Optional[Set[Card]],
    ) -> Card:
        """The most sophisticated Brave Rats AI ever written
        Expects to be called once each time a card needs to be played, and once after the game is over.

        :param player: a Player instance
        :param game: a Game instance, used to look up info about played cards, score, etc.
        :param spied_card: If I successfully played a spy last turn, this is the card that the opponent has revealed and
            will play. Otherwise, None
        :return: a card from my player's hand with which to vanquish my opponent, or None if the game is over
        """
        return random.choice(player.hand)

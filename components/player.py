from typing import Optional, Set, List

from brains.Brain import Brain
from components import cards
from components.cards import Card, Color
from components.game_status import GameStatus


class CheatingException(Exception):
    pass


class Player(object):
    def __init__(self, color: Color, brain: Brain, hand: List[Card] = None):
        """
        :param color: a Color enum value indicating which color this player is playing for
        :param game: a GameStatus object
        :param brain_fn: The brains of the operation. See example_ai.py for an example.
            Should be a function which takes two required inputs:
            player: a Player instance used for accessing the player's hand
            game: a GameStatus instance for accessing game details
             and one optional input:
            spied_card: if player successfully played a spy the previous turn, this will be the card that the other
                player has revealed to play.
            Should return a card from its hand to play. Can harbor hidden powers; should be expected to be called
                exactly once per round.
        :param hand_str: string of card values in initial hand (eg. '0123456' to play without Prince)
        """
        self.hand = hand if hand else [card for card in Card]
        self.color = color
        self.brain = brain

    def has_cards(self) -> bool:
        return bool(len(self.hand))

    def choose_and_play_card(
        self,
        game: GameStatus,
        spied_card: Optional[Card] = None,
        opponent_hand: Optional[Set[Card]] = None,
    ) -> Card:
        card = self.brain.play_turn(self, game, spied_card, opponent_hand)
        if card not in self.hand:
            raise CheatingException(
                "{} tried to play card {} which is not in hand {}".format(
                    self.brain, card, self.hand
                )
            )
        self.hand.remove(card)
        return card

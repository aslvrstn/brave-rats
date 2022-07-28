from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Set

if TYPE_CHECKING:
    from components.cards import Card
    from components.game_status import GameStatus
    from components.player import Player


class Brain:
    def play_turn(
        self,
        player: Player,
        game: GameStatus,
        spied_card: Optional[Card],
        opponent_hand: Optional[Set[Card]],
    ) -> Card:
        raise NotImplementedError()

from typing import List, Tuple

from components.cards import Card, Color

# Game ends when players have played all of their cards, so the max number of rounds
# in the game is the size of the players' initial hand.
from components.fight import QUICK_FIGHT_RESULT, FightResult


class GameStatus(object):
    def __init__(
        self,
        points_to_win: int = 4,
        red_points: int = 0,
        blue_points: int = 0,
        resolved_fights: List[Tuple] = None,
        on_hold_fights: List[Tuple] = None,
    ):
        self.points_to_win = points_to_win
        self.red_points, self.blue_points = red_points, blue_points

        # List of tuples of (red_card, blue_card)
        # Doesn't include on hold fights; use all_fights for full list
        self.resolved_fights = resolved_fights.copy() if resolved_fights else []
        self.on_hold_fights = on_hold_fights.copy() if on_hold_fights else []

    def __str__(self):
        return f"r: {self.red_points} b: {self.blue_points}, held: {self.on_hold_fights}"

    def clone(self):
        return GameStatus(
            self.points_to_win, self.red_points, self.blue_points, self.resolved_fights, self.on_hold_fights
        )

    @property
    def on_hold_points(self):
        two_pointers = [
            (red_card, blue_card)
            for red_card, blue_card in self.on_hold_fights
            if red_card == Card.ambassador and blue_card == Card.ambassador
        ]
        return len(self.on_hold_fights) + len(two_pointers)

    @property
    def winner(self):
        if self.red_points >= self.points_to_win:
            return Color.red
        if self.blue_points >= self.points_to_win:
            return Color.blue
        return None

    @property
    def most_recent_fight(self):
        if self.on_hold_fights:
            return self.on_hold_fights[-1]
        if self.resolved_fights:
            return self.resolved_fights[-1]
        return None, None

    # Like `most_recent_fight`, but always (your_card, opponent_card)
    def recent_fight_for(self, color: Color):
        rec = self.most_recent_fight
        return rec if color == Color.red else reversed(rec)

    @property
    def score_summary(self):
        player_scores = "points: red {} to blue {}".format(
            self.red_points, self.blue_points
        )
        if self.on_hold_points:
            return player_scores + " with {} points on hold".format(self.on_hold_points)
        return player_scores

    def resolve_fight(self, red_card, blue_card):
        """Given a fight, updates the game state according to the resolution of that fight
        :param red_card: Card enum value played by red player
        :param blue_card: Card enum value played by blue player
        :param game: GameStatus instance to be updated
        """
        previous_red_card, previous_blue_card = self.most_recent_fight

        # Using QUICK_FIGHT_RESULT is equivalent to this, but all the answers have been cached off
        # result = fight_result(red_card, blue_card, previous_red_card, previous_blue_card)
        result = QUICK_FIGHT_RESULT[
            (red_card, blue_card, previous_red_card, previous_blue_card)
        ]

        if result is FightResult.on_hold:
            self.on_hold_fights.append((red_card, blue_card))
        else:
            self.resolved_fights.extend(self.on_hold_fights)
            self.resolved_fights.append((red_card, blue_card))
            points_from_on_hold = self.on_hold_points
            self.on_hold_fights = []

        if result in {FightResult.red_wins, FightResult.red_wins_2}:
            extra_point = 1 if result is FightResult.red_wins_2 else 0
            self.red_points += 1 + points_from_on_hold + extra_point

        if result in {FightResult.blue_wins, FightResult.blue_wins_2}:
            extra_point = 1 if result is FightResult.blue_wins_2 else 0
            self.blue_points += 1 + points_from_on_hold + extra_point

        # If you win by princess, just max out the scoreboard
        if result == FightResult.red_wins_game:
            self.red_points = 999999
        if result == FightResult.blue_wins_game:
            self.blue_points = 999999

        return result

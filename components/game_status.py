from components.cards import Card, Color

# Game ends when players have played all of their cards, so the max number of rounds
# in the game is the size of the players' initial hand.
POINTS_TO_WIN = 4


class GameStatus(object):
    def __init__(self):
        self.red_points, self.blue_points = 0, 0

        # List of tuples of (red_card, blue_card)
        self.resolved_fights = []  # Doesn't include on hold fights; use all_fights for full list
        self.on_hold_fights = []

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
        if self.red_points >= POINTS_TO_WIN:
            return Color.red
        if self.blue_points >= POINTS_TO_WIN:
            return Color.blue
        return None

    @property
    def most_recent_fight(self):
        if self.on_hold_fights:
            return self.on_hold_fights[-1]
        if self.resolved_fights:
            return self.resolved_fights[-1]
        return None, None

    @property
    def score_summary(self):
        player_scores = "points: red {} to blue {}".format(
            self.red_points, self.blue_points
        )
        if self.on_hold_points:
            return player_scores + " with {} points on hold".format(self.on_hold_points)
        return player_scores

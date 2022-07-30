import itertools
from enum import IntEnum

from components.cards import Card, Color, initial_hand

# Ordered by ascending goodness for blue.
# Note that I'm gradually reducing the places where "color" matters, so think of
# "red" as player1 and "blue" as player2 in any calls that produce one of these
FightResult = IntEnum(
    "FightResult",
    "blue_wins_game blue_wins_2 blue_wins on_hold red_wins red_wins_2 red_wins_game",
)


def _short_format_result(fight_result_):
    """returns a one- to two-character representation of a FightResult"""
    return {
        FightResult.red_wins: "r",
        FightResult.blue_wins: "b",
        FightResult.red_wins_2: "r2",
        FightResult.blue_wins_2: "b2",
        FightResult.on_hold: "h",
    }[fight_result_]


def fight_result(red_card, blue_card, prev_red_card, prev_blue_card):
    """The main game engine. Figures out what the result of played cards should be.
    :return: a FightResult
    """
    # 5. Wizard - nullifies opponent's power
    blue_has_power = red_card != Card.wizard
    red_has_power = blue_card != Card.wizard

    # 0. Musician - round is put on hold
    if red_has_power and red_card == Card.musician:
        return FightResult.on_hold
    if blue_has_power and blue_card == Card.musician:
        return FightResult.on_hold

    # 1. Princess - wins against prince
    if red_has_power and red_card == Card.princess and blue_card == Card.prince:
        return FightResult.red_wins_game
    if blue_has_power and blue_card == Card.princess and red_card == Card.prince:
        return FightResult.blue_wins_game

    # 7. Prince - you win the round
    if red_has_power and red_card == Card.prince and blue_card != Card.prince:
        return FightResult.red_wins
    if blue_has_power and blue_card == Card.prince and red_card != Card.prince:
        return FightResult.blue_wins

    # 6. General - next round, your card gets +2 strength
    if prev_red_card == Card.general and prev_blue_card not in [
        Card.wizard,
        Card.musician,
    ]:
        red_value = red_card.value + 2
    else:
        red_value = red_card.value
    if prev_blue_card == Card.general and prev_red_card not in [
        Card.wizard,
        Card.musician,
    ]:
        blue_value = blue_card.value + 2
    else:
        blue_value = blue_card.value

    # 3. Assassin - Lowest strength wins
    modifier = (
        -1
        if (red_has_power and red_card == Card.assassin)
        or (blue_has_power and blue_card == Card.assassin)
        else 1
    )

    if modifier * red_value > modifier * blue_value:
        # 4. Ambassador - win with this counts as 2 victories
        if red_has_power and red_card == Card.ambassador:
            return FightResult.red_wins_2
        return FightResult.red_wins
    elif modifier * red_value < modifier * blue_value:
        # 4. Ambassador - win with this counts as 2 victories
        if blue_has_power and blue_card == Card.ambassador:
            return FightResult.blue_wins_2
        return FightResult.blue_wins
    else:
        return FightResult.on_hold


# Cache off all possible values of fight_result for a fetch-speed gain
QUICK_FIGHT_RESULT = {
    cards_: fight_result(*cards_)
    for cards_ in itertools.product(
        *[initial_hand()] * 2 + [initial_hand() + [None]] * 2
    )
}


def print_results_table(red_general_played=False):
    """Prints a results table similar to that provided with the Brave Rats card game.
    :param red_general_played: if True,
    :return: None; output is printed to stdout
    """
    format_cell = "{}".format
    previous_red = Card.general if red_general_played else None

    # Table header
    print(" ", "\t", "\t".join("b=" + format_cell(card.value) for card in Card))

    for red_card in Card:
        print(
            "\t".join(
                ["r=" + format_cell(red_card.value)]
                + [  # Row header
                    format_cell(
                        _short_format_result(
                            fight_result(red_card, blue_card, previous_red, None)
                        )
                    )
                    for blue_card in Card
                ]
            )
        )


def successful_spy_color(xxx_todo_changeme):
    """Determine whether the provided fight has a non-nullified spy in it
    Takes a fight tuple of (red_card, blue_card)
    :return: Color of non-nullified spy, if any, or None if no non-nullified spy.
    """
    (red_card, blue_card) = xxx_todo_changeme
    spy_nullifiers = {Card.musician, Card.wizard, Card.spy}
    if red_card == Card.spy and blue_card not in spy_nullifiers:
        return Color.red
    if blue_card == Card.spy and red_card not in spy_nullifiers:
        return Color.blue
    return None

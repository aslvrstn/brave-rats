from enum import IntEnum


class Card(IntEnum):
    musician = 0
    princess = 1
    spy = 2
    assassin = 3
    ambassador = 4
    wizard = 5
    general = 6
    prince = 7

    @classmethod
    def get_from_int(cls, n):
        return next((item for item in cls if item.value is n))


# Use IntEnum, not Enum, here, to prevent bug #15: "Loaded brain functions have wiiiiiierd behavior"
Color = IntEnum("Color", "red blue")

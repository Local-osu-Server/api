from enum import IntEnum


class GameMode(IntEnum):
    STANDARD = 0
    TAIKO = 1
    CTB = 2
    MANIA = 3


class CustomGameMode(IntEnum):
    VANILLA = 0
    RELAX = 1
    AUTOPILOT = 2

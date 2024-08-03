from typing import Any


NAME = 1
LEVEL = 3
QUALITY = 4
BREED = 5
FAMILY = 6
COLLECTED = 9
ABILITY_START = 10
BASE_HEALTH = 16
BASE_POWER = 17
BASE_SPEED = 18
CAN_BATTLE = 24

YES = "Yes"
NO = "No"

UNKNOWN = "Unknown"


def row_is_valid(row: tuple[Any, ...]) -> bool:
    if row[CAN_BATTLE] != YES:
        return False
    if any([x == UNKNOWN for x in row]):
        return False
    if any([x is None for x in row[ABILITY_START : ABILITY_START + 5]]):
        return False

    return True

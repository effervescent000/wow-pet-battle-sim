from enum import Enum
from typing import Literal


Families = Literal[
    "Magic",
    "Beast",
    "Dragonkin",
    "Undead",
    "Flying",
    "Critter",
    "Humanoid",
    "Mechanical",
    "Elemental",
    "Aquatic",
]

Breeds = Literal["BB", "PB", "SB", "HB", "PP", "PS", "PH", "SS", "HS", "HH", "HP"]

Quality = Literal["Common", "Uncommon", "Rare", "Epic", "Legendary", "Poor"]

Priority = Enum(
    "Priority",
    ["DamageOnly", "DamageWithModifier", "EnemyModifier", "Heal", "FriendlyModifier"],
)


BREED_POINTS = {
    "PP": (0, 20, 0),
    "SS": (0, 0, 20),
    "HH": (20, 0, 0),
    "HP": (9, 9, 0),
    "PS": (0, 9, 9),
    "HS": (9, 0, 9),
    "PB": (4, 9, 4),
    "SB": (4, 4, 9),
    "HB": (9, 4, 4),
    "BB": (5, 5, 5),
}

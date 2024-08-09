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

Quality = Literal["Common", "Uncommon", "Rare", "Epic", "Legendary"]

Priority = Enum(
    "Priority",
    ["DamageOnly", "DamageWithModifier", "EnemyModifier", "Heal", "FriendlyModifier"],
)

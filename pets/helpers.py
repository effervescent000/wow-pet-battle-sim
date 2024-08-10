from typing import Literal
from pets.constants import BREED_POINTS, Breeds, Quality


def get_stat_location(stat: Literal["health", "power", "speed"]) -> int:
    match stat:
        case "health":
            return 0
        case "power":
            return 1
        case "speed":
            return 2


def get_breed_points(breed: Breeds, stat: Literal["health", "power", "speed"]) -> int:
    return BREED_POINTS[breed][get_stat_location(stat)]


def get_quality_modifier(quality: Quality) -> float:
    match quality:
        case "Rare":
            return 1.3
        case "Uncommon":
            return 1.2
        case "Common":
            return 1.1
        case "Poor":
            return 1.0
        case "Epic":
            return 1.4
        case "Legendary":
            return 2.0

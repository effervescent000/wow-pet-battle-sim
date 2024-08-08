from typing import Any


def sort_pets_with_actions(
    pets_with_actions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return sorted(pets_with_actions, key=lambda pet: pet["pet"].speed, reverse=True)

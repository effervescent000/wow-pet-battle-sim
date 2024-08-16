from typing import Callable
from pydantic import BaseModel

from pets.models import Modifier, PetInstance


class ConditionKwargs(BaseModel):
    modifierChecks: list[Callable[["PetInstance", "PetInstance"], bool]] = []


def always_use(*args) -> bool:
    return True


def standard_checks(
    actor: "PetInstance", target: "PetInstance", kwargs: "ConditionKwargs"
) -> bool:
    if kwargs.modifierChecks:
        if not all(check(actor, target) for check in kwargs.modifierChecks):
            return False
    return True


def is_modifier_present(target: "PetInstance", modifier: "Modifier") -> bool:
    if modifier in target.modifiers:
        return True
    return False

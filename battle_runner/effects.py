from battle_runner import log_models
from pets.models import Modifier, PetInstance


def apply_to_user(
    actor: "PetInstance", _target: "PetInstance", modifier: "Modifier"
) -> log_models.EffectChange:
    actor.add_modifier(modifier)
    return log_models.EffectChange(
        target=actor.label,
        change="add",
        effect=modifier.name,
    )


def apply_to_target(
    _actor: "PetInstance", target: "PetInstance", modifier: "Modifier"
) -> log_models.EffectChange | None:
    target.add_modifier(modifier)
    return log_models.EffectChange(
        target=target.label,
        change="add",
        effect=modifier.name,
    )

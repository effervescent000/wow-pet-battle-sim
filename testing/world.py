from battle_runner.effects import apply_to_user
from pets.constants import Priority
from pets.models import (
    DamageAbility,
    DamageAbilityWithModifier,
    Modifier,
    StatAdjustment,
    Value,
)


abilities = [
    DamageAbility(
        name="FakeTestAbilityNeverUse",
        family="Beast",
        damage_value=Value(base_value=20),
        priority=Priority.Heal,
        conditions=[lambda *args: False],
    ),
    DamageAbilityWithModifier(
        name="FakeTestWithBuff",
        family="Beast",
        damage_value=Value(base_value=20),
        effects=[
            lambda actor, target: apply_to_user(
                actor,
                target,
                modifier=Modifier(
                    name="Test Buff",
                    duration=3,
                    stat_adjustments=[StatAdjustment(stat="power", value=5)],
                ),
            )
        ],
    ),
    DamageAbility(name="Claw", family="Beast", damage_value=Value(base_value=20)),
]

AbilityLookup = {ability.name: ability for ability in abilities}

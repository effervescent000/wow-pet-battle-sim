from pets.constants import Priority
from pets.models import DamageAbility, Value


abilities = [
    DamageAbility(name="Claw", damage_value=Value(base_value=20)),
    DamageAbility(
        name="FakeTestAbility",
        damage_value=Value(base_value=20),
        priority=Priority.Heal,
        conditions=[lambda *args: False],
    ),
]

AbilityLookup = {ability.name: ability for ability in abilities}

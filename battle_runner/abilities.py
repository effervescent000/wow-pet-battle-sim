from pets import models


abilities = [
    models.DamageAbility(name="Claw", damage_value=models.Value(base_value=20)),
    models.DamageAbility(
        name="FakeTestAbility",
        damage_value=models.Value(base_value=20),
        priority=models.Priority.Heal,
        conditions=[lambda *args: False],
    ),
]

AbilityLookup = {ability.name: ability for ability in abilities}

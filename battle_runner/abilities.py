from pets import models as m


abilities = [
    m.DamageAbility(name="Claw", damage_value=m.Value(base_value=20)),
    m.DamageAbility(
        name="FakeTestAbility",
        damage_value=m.Value(base_value=20),
        priority=m.Priority.Heal,
        conditions=[lambda *args: False],
    ),
]

AbilityLookup = {ability.name: ability for ability in abilities}

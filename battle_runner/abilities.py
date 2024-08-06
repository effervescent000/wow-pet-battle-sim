from pets import models


abilities = [
    models.DamageAbility(name="Claw", damage_value=models.Value(base_value=20))
]

AbilityLookup = {ability.name: ability for ability in abilities}

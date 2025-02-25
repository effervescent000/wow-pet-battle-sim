# from pets.constants import Priority
from pets.models import DamageAbility, Value


abilities = [
    DamageAbility(name="Claw", family="Beast", damage_value=Value(base_value=20)),
]

AbilityLookup = {ability.name: ability for ability in abilities}

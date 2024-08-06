from battle_runner.abilities import AbilityLookup
from pets.models import PetInstance, PetSpecies, Stats


def test_fetch_ability_from_location_key() -> None:
    pet_instance = PetInstance(
        breed="BB",
        level=1,
        quality="Common",
        species=PetSpecies(
            name="Test Pet",
            family="Humanoid",
            base_stats=Stats(health=100, power=100, speed=100),
            abilities=["Claw", "Another", "test", "ability", "something", "six"],
        ),
        cur_health=100,
        active_skills_by_location=(1, 2, 3),
    )
    assert pet_instance.active_skills == (AbilityLookup.get("Claw"), None, None)

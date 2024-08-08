from pets.models import PetInstance, PetSpecies, Stats


def pet_species_factory() -> PetSpecies:
    return PetSpecies(
        name="Test Pet",
        family="Humanoid",
        base_stats=Stats(health=100, power=100, speed=100),
        abilities=[
            "Claw",
            "FakeTestAbility",
            "test",
            "ability",
            "something",
            "six",
        ],
    )


def pet_factory(
    level: int | None = None, species: PetSpecies | None = None
) -> PetInstance:
    return PetInstance(
        level=level or 25,
        species=species or pet_species_factory(),
        breed="BB",
        quality="Rare",
        cur_health=100,
        active_skills_by_location=(1, 2, 3),
    )

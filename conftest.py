from unittest.mock import patch
import pytest

from pets.db import PetDB
from pets.shapes import pet_factory, pet_species_factory
from testing import world


@pytest.fixture
def db():
    db = PetDB()
    db.player_pet_roster = [
        pet_factory(species=pet_species_factory(family="Magic")),
        pet_factory(species=pet_species_factory(family="Beast")),
        pet_factory(species=pet_species_factory(family="Dragonkin")),
        pet_factory(species=pet_species_factory(family="Humanoid")),
        pet_factory(species=pet_species_factory(family="Humanoid")),
        pet_factory(species=pet_species_factory(family="Humanoid")),
    ]
    return db


@pytest.fixture(autouse=True)
def patch_abilities():
    with patch.dict("battle_runner.abilities.AbilityLookup", world.AbilityLookup):
        yield

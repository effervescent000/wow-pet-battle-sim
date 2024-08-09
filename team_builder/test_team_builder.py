import pytest
from pets.db import PetDB

from team_builder.team_builder import TeamBuilder, TeamBuildingError


def test_get_available_pets_basic(db: "PetDB"):
    """Available pet roster == all player pets when no family is given."""
    team_builder = TeamBuilder(db)
    available_pets = team_builder._get_available_pets()
    assert len(available_pets) == len(db.player_pet_roster)


def test_not_enough_pets(db: "PetDB"):
    """Raises error when not enough pets are found."""
    team_builder = TeamBuilder(db, "Magic")
    with pytest.raises(TeamBuildingError):
        team_builder._get_available_pets()


def test_get_available_pets_family(db: "PetDB"):
    """Available pet roster == all player pets of the given family."""
    team_builder = TeamBuilder(db, "Humanoid")
    available_pets = team_builder._get_available_pets()
    assert all(x.species.family == "Humanoid" for x in available_pets)


def test_choose_pets(db: "PetDB"):
    """Chooses pets from the available roster."""
    team_builder = TeamBuilder(db, "Humanoid")
    available_pets = team_builder._get_available_pets()
    team = team_builder._choose_pets(available_pets)
    assert len(team) == 3

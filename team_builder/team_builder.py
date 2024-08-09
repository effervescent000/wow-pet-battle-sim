import random
from pets.db import PetDB
from pets.models import Pet, PetInstance


class TeamBuildingError(Exception):
    pass


class TeamBuilder:
    def __init__(self, db: PetDB, target_family: str | None = None):
        self.db = db
        self.target_family = target_family

    def build_team(self) -> list[PetInstance]:
        available_pets: list[Pet] = []
        if self.target_family:
            available_pets = [
                pet
                for pet in self.db.player_pet_roster
                if pet.species.family == self.target_family
            ]
        else:
            available_pets = [*self.db.player_pet_roster]

        if len(available_pets) < 3:
            raise TeamBuildingError("Not enough pets to build a team")

        chosen_pets: list[PetInstance] = []
        while len(chosen_pets) < 3:
            choice = random.choice(available_pets)
            chosen_pets.append(
                choice.make_instance(
                    (
                        random.choice([1, 4]),
                        random.choice([2, 5]),
                        random.choice([3, 6]),
                    )
                )
            )
            available_pets.remove(choice)

        return chosen_pets

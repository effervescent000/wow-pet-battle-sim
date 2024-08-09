import random
from pets.constants import Families
from pets.db import PetDB
from pets.models import Pet, PetInstance


class TeamBuildingError(Exception):
    pass


class TeamBuilder:
    def __init__(self, db: PetDB, target_family: Families | None = None):
        self.db = db
        self.target_family = self._process_family(target_family)

    def _process_family(self, family: str | None) -> Families | None:
        if family is None:
            return None
        match family.lower():
            case "humanoid":
                return "Humanoid"
            case "human":
                return "Humanoid"
            case "hu":
                return "Humanoid"

            case "magic":
                return "Magic"
            case "mag":
                return "Magic"
            case "ma":
                return "Magic"

            case "aquatic":
                return "Aquatic"
            case "aqua":
                return "Aquatic"
            case "aq":
                return "Aquatic"
            case "water":
                return "Aquatic"

            case "beast":
                return "Beast"
            case "bst":
                return "Beast"
            case "b":
                return "Beast"

            case "dragonkin":
                return "Dragonkin"
            case "dragon":
                return "Dragonkin"
            case "drg":
                return "Dragonkin"
            case "d":
                return "Dragonkin"

            case "undead":
                return "Undead"
            case "und":
                return "Undead"
            case "u":
                return "Undead"

            case "flying":
                return "Flying"
            case "fly":
                return "Flying"
            case "fl":
                return "Flying"

            case "critter":
                return "Critter"
            case "crt":
                return "Critter"
            case "c":
                return "Critter"

            case "mechanical":
                return "Mechanical"
            case "mech":
                return "Mechanical"
            case "me":
                return "Mechanical"

            case "elemental":
                return "Elemental"
            case "ele":
                return "Elemental"

            case _:
                raise TeamBuildingError(f"Invalid family: {family}")

    def _get_available_pets(self) -> list[Pet]:
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

        return available_pets

    def _choose_pets(self, available_pets: list[Pet]) -> list[PetInstance]:
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

    def build_team(self) -> list[PetInstance]:
        available_pets = self._get_available_pets()
        chosen_pets = self._choose_pets(available_pets)
        return chosen_pets

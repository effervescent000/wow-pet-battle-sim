from pets.models import Pet, PetSpecies


class PetDB:
    def __init__(self) -> None:
        self.player_pet_roster: list[Pet] = []
        self.species: list[PetSpecies] = []

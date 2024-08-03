from pets.models import Pet, PetSpecies


class PetDB:
    def __init__(self) -> None:
        self.pets: list[Pet] = []
        self.species: list[PetSpecies] = []

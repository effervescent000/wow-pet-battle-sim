from pets.models import PetInstance


class BattleRunner:
    def __init__(
        self,
        player_pets: tuple[PetInstance, PetInstance, PetInstance],
        rival_pets: tuple[PetInstance, PetInstance, PetInstance],
    ):
        self.player_pets = player_pets
        self.rival_pets = rival_pets
        self.round = 0

        self.active_player_pet = self.player_pets[0]
        self.active_rival_pet = self.rival_pets[0]

    def do_round(self) -> None:
        self.round += 1

        # first, figure out which pet should even go first on each round
        active_pets = [self.active_player_pet, self.active_rival_pet]
        active_pets.sort(key=lambda pet: pet.speed, reverse=True)

        for pet in active_pets:
            pet.increment_modifiers()

        # second, select actions (which we're glossing over for now)

        # third, remove modifiers that have expired
        for pet in active_pets:
            pet.clean_modifiers()

    def choose_action(self, pet: PetInstance) -> None:
        pass

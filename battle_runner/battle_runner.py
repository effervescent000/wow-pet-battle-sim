from typing import cast

from battle_runner.helpers import sort_pets_with_actions
from pets.models import Ability, PetInstance


class BattleRunner:
    def __init__(
        self,
        player_pets: tuple[PetInstance, ...],
        rival_pets: tuple[PetInstance, ...],
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
        # active_pets.sort(key=lambda pet: pet.speed, reverse=True)

        for pet in active_pets:
            pet.increment_modifiers()

        # second, select actions (which we're glossing over for now)
        player_pet_action = self.active_player_pet.select_ability(self.active_rival_pet)
        rival_pet_action = self.active_rival_pet.select_ability(self.active_player_pet)

        pets_with_actions = [
            {"pet": self.active_player_pet, "action": player_pet_action},
            {"pet": self.active_rival_pet, "action": rival_pet_action},
        ]
        pets_with_actions = sort_pets_with_actions(pets_with_actions)

        for x in pets_with_actions:
            action, target = x["action"]
            if action is None:
                continue
            action = cast(Ability, action)
            action.do_action(x["pet"], target)

        # third, remove modifiers that have expired
        for pet in active_pets:
            pet.clean_modifiers()

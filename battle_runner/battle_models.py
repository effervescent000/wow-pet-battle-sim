from pydantic import BaseModel, computed_field

from pets import models as pet_models
from pets.constants import Families, Quality


class RivalPet(BaseModel):
    name: str
    family: Families
    quality: Quality
    abilities: list[str]
    stats: pet_models.Stats

    @property
    def speed(self) -> float:
        return self.stats.speed

    @property
    def health(self) -> float:
        return self.stats.health

    @property
    def power(self) -> float:
        return self.stats.power

    @computed_field()
    @property
    def active_skills(self) -> tuple[pet_models.Ability | None, ...]:
        from battle_runner import abilities as ab

        return tuple(ab.AbilityLookup.get(ability) for ability in self.abilities)


class Rival(BaseModel):
    name: str
    aliases: list[str] = []
    pets: tuple[RivalPet, RivalPet, RivalPet]

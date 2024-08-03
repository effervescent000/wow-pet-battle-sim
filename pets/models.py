from typing import Literal
from pydantic import BaseModel

Families = Literal[
    "Magic",
    "Beast",
    "Dragonkin",
    "Human",
    "Undead",
    "Flying",
    "Critter",
    "Humanoid",
    "Mechanical",
    "Elemental",
    "Aquatic",
]

Breeds = Literal["BB", "PB", "SB", "HB", "PP", "PS", "PH", "SS", "HS", "HH", "HP"]

Quality = Literal["Common", "Uncommon", "Rare", "Epic", "Legendary"]


class Ability(BaseModel):
    name: str
    base_damage: float | None = None
    base_healing: float | None = None
    base_damage_reduction: float | None = None


class PetSpecies(BaseModel):
    name: str
    family: Families
    base_health: float
    base_power: float
    base_speed: float
    abilities: list[Ability]

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PetSpecies) and self.name == other.name


class Pet(BaseModel):
    label: str | None = None
    breed: Breeds
    level: int
    quality: Quality
    species: PetSpecies

    def __hash__(self) -> int:
        return hash(self.label or (self.breed, self.level, self.species))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pet):
            return False
        if self.label is not None and other.label is not None:
            return self.label == other.label
        if (
            self.breed == other.breed
            and self.level == other.level
            and self.species == other.species
        ):
            return True
        return False

    @property
    def max_health(self) -> float:
        # XXX I don't know what the math for this actually is
        return self.species.base_health * self.level


class PetInstance(Pet):
    cur_health: float
    active_skills: tuple[int, int, int]

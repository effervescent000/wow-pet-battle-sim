from __future__ import annotations
from enum import Enum
from functools import total_ordering

from typing import Callable, Literal
from pydantic import BaseModel, computed_field, field_validator

from battle_runner import abilities as ab
from battle_runner import log_models as battle_models

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

Priority = Enum(
    "Priority",
    ["DamageOnly", "DamageWithModifier", "EnemyModifier", "Heal", "FriendlyModifier"],
)


class Modifier(BaseModel):
    name: str
    duration: int


class Value(BaseModel):
    base_value: float
    scale_factor: float = 1

    def calc_value(self, power: float) -> float:
        return self.base_value + self.scale_factor * power


@total_ordering
class Ability(BaseModel):
    name: str
    priority: Priority
    # effects should be callbacks that take the actor and the target
    # and apply the modifiers as appropriate
    effects: list[Callable[["PetInstance", "PetInstance"], None]] = []
    conditions: list[Callable[["PetInstance", "PetInstance"], bool]] = []

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ability) and self.name == other.name

    def __lt__(self, other: "Ability") -> bool:
        return self.priority.value < other.priority.value

    def do_action(
        self, actor: "PetInstance", target: "PetInstance"
    ) -> battle_models.BattleEvent:
        raise NotImplementedError()


class DamageAbility(Ability):
    hit_chance: float = 1
    damage_value: Value
    priority: Priority = Priority.DamageOnly
    conditions: list[Callable[["PetInstance", "PetInstance"], bool]] = [
        lambda *args: True
    ]

    def do_action(
        self, actor: "PetInstance", target: "PetInstance"
    ) -> battle_models.BattleEvent:
        damage = self.damage_value.calc_value(actor.power)
        event = battle_models.BattleEvent(
            actor=actor.label or actor.species.name,
            target=target.label or target.species.name,
            result=[
                battle_models.DamageOrHealing(
                    amount=damage, ability=self.name, type="damage"
                )
            ],
        )
        return event


class Stats(BaseModel):
    health: float
    power: float
    speed: float


class PetSpecies(BaseModel):
    name: str
    family: Families
    base_stats: Stats
    abilities: list[str]

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
        return self.species.base_stats.health * self.level

    def make_instance(self, active_skills: tuple[int, int, int]) -> "PetInstance":
        return PetInstance(
            label=self.label,
            breed=self.breed,
            level=self.level,
            quality=self.quality,
            species=self.species,
            cur_health=self.max_health,
            active_skills_by_location=active_skills,
        )


class PetInstance(Pet):
    cur_health: float
    active_skills_by_location: tuple[int, int, int]
    modifiers: list[Modifier] = []

    @computed_field()
    @property
    def active_skills(self) -> tuple[Ability | None, ...]:
        return tuple(
            ab.AbilityLookup.get(self.species.abilities[i - 1])
            if self.species.abilities[i - 1] is not None
            else None
            for i in self.active_skills_by_location
        )

    @field_validator("active_skills")
    def validate_active_skills(cls, v: tuple[int, int, int]) -> tuple[int, int, int]:
        if not (v[0] == 1 ^ v[0] == 4):
            raise ValueError("Invalid active skill")
        return v

    @property
    def speed(self) -> float:
        # TODO figure out actual math + include effects of modifiers
        return self.species.base_stats.speed * self.level

    @property
    def power(self) -> float:
        # TODO figure out actual math + include effects of modifiers
        return self.species.base_stats.power * self.level

    def increment_modifiers(self) -> None:
        for mod in self.modifiers:
            mod.duration -= 1

    def clean_modifiers(self) -> None:
        self.modifiers = [mod for mod in self.modifiers if mod.duration > 0]

    def select_ability(
        self, target: PetInstance
    ) -> tuple[Ability | None, PetInstance | None]:
        abilities = sorted(
            [x for x in self.active_skills if x is not None], reverse=True
        )
        for x in abilities:
            if all(cond(self, target) for cond in x.conditions):
                return (x, target)
        return (None, None)

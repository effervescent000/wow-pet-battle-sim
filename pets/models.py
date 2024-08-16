from __future__ import annotations
from functools import total_ordering

from typing import Callable, Literal, cast
from pydantic import BaseModel, computed_field, field_validator


from battle_runner import log_models
from pets.constants import Breeds, Families, Priority, Quality
from pets.helpers import get_breed_points, get_quality_modifier


class StatModifier(BaseModel):
    stat: Literal["health", "power", "speed", "damage_out", "damage_in"]
    value: float


class StatAdjustment(StatModifier):
    """Used for flat bonuses/penalties"""


class StatFactor(StatModifier):
    """Used for multipliers"""


class MinimalModifier(BaseModel):
    name: str

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MinimalModifier) and self.name == other.name


class Modifier(MinimalModifier):
    name: str
    duration: int
    stat_adjustments: list[StatAdjustment] = []
    stat_factors: list[StatFactor] = []


class Value(BaseModel):
    base_value: float
    scale_factor: float = 1

    def calc_value(self, power: float) -> float:
        return self.base_value + self.scale_factor * power


@total_ordering
class Ability(BaseModel):
    name: str
    priority: Priority
    family: Families
    # effects should be callbacks that take the actor and the target
    # and apply the modifiers as appropriate
    effects: list[
        Callable[["PetInstance", "PetInstance"], log_models.EffectChange]
    ] = []
    conditions: list[Callable[["PetInstance", "PetInstance"], bool]] = []

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Ability) and self.name == other.name

    def __lt__(self, other: "Ability") -> bool:
        return self.priority.value < other.priority.value

    def do_action(
        self, actor: "PetInstance", target: "PetInstance"
    ) -> log_models.BattleEvent:
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
    ) -> log_models.BattleEvent:
        damage = self.damage_value.calc_value(actor.power)
        target.cur_health -= damage
        event = log_models.BattleEvent(
            actor=actor.label or actor.species.name,
            target=target.label or target.species.name,
            result=[
                log_models.DamageOrHealing(
                    amount=damage, ability=self.name, type="damage"
                )
            ],
        )
        return event


class DamageAbilityWithModifier(DamageAbility):
    effects: list[
        Callable[["PetInstance", "PetInstance"], log_models.EffectChange | None]
    ]

    def do_action(
        self, actor: "PetInstance", target: "PetInstance"
    ) -> log_models.BattleEvent:
        event = super().do_action(actor, target)
        changes: list[log_models.EffectChange] = []
        for effect in self.effects:
            result = effect(actor, target)
            if result is not None:
                changes.append(result)
        event.effects = changes
        return event


class Stats(BaseModel):
    health: float
    power: float
    speed: float


class PetSpecies(BaseModel):
    name: str
    family: Families
    base_stats: Stats
    abilities: list[str | None]

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, PetSpecies) and self.name == other.name

    @field_validator("abilities")
    def abilities_are_correct_length(cls, v: list[str | None]) -> list[str | None]:
        if len(v) != 6:
            raise ValueError("Pet species must have exactly 6 abilities")
        return v


class Pet(BaseModel):
    nickname: str | None = None
    breed: Breeds
    level: int
    quality: Quality
    species: PetSpecies

    @computed_field()
    @property
    def label(self) -> str:
        return self.nickname or self.species.name

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
        return (
            (
                self.species.base_stats.health
                + get_breed_points(self.breed, "health") / 10
            )
            * 5
            * self.level
            * get_quality_modifier(self.quality)
        ) + 100

    def make_instance(self, active_skills: tuple[int, int, int]) -> "PetInstance":
        return PetInstance(
            nickname=self.label,
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
        from battle_runner.abilities import AbilityLookup

        return tuple(
            AbilityLookup.get(cast(str, self.species.abilities[i - 1]))
            if self.species.abilities[i - 1] is not None
            else None
            for i in self.active_skills_by_location
        )

    @field_validator("active_skills_by_location")
    def validate_active_skills(cls, v: tuple[int, int, int]) -> tuple[int, int, int]:
        if not (bool(v[0] == 1) ^ bool(v[0] == 4)):
            raise ValueError("Invalid active skill")
        return v

    @property
    def speed(self) -> float:
        return (
            (self.species.base_stats.speed + get_breed_points(self.breed, "speed") / 10)
            * self.level
            * get_quality_modifier(self.quality)
            + self.get_final_stat_adjustment("speed")
        ) * self.get_final_stat_factor("speed")

    @property
    def power(self) -> float:
        return (
            (self.species.base_stats.power + get_breed_points(self.breed, "power") / 10)
            * self.level
            * get_quality_modifier(self.quality)
            + self.get_final_stat_adjustment("power")
        ) * self.get_final_stat_factor("power")

    def get_final_stat_adjustment(
        self, stat: Literal["health", "power", "speed", "damage_out", "damage_in"]
    ) -> float:
        return sum(
            adj.value
            for mod in self.modifiers
            for adj in mod.stat_adjustments
            if adj.stat == stat
        )

    def get_final_stat_factor(
        self, stat: Literal["health", "power", "speed", "damage_out", "damage_in"]
    ) -> float:
        return sum(
            fac.value
            for mod in self.modifiers
            for fac in mod.stat_factors
            if fac.stat == stat
        )

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

    def add_modifier(self, modifier: Modifier) -> None:
        self.modifiers.append(modifier)

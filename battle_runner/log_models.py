from __future__ import annotations

from typing import Literal
from pydantic import BaseModel


class DamageOrHealing(BaseModel):
    ability: str
    amount: float | None = None
    type: Literal["damage", "healing"] | None = None


class EffectChange(BaseModel):
    effect: str
    target: str
    change: Literal["add", "remove"]


class BattleEvent(BaseModel):
    round: int | None = None
    actor: str
    target: str
    result: list[DamageOrHealing]
    effects: list[EffectChange] = []


class BattleLog(BaseModel):
    events: list[BattleEvent] = []

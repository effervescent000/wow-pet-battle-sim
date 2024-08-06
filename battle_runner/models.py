from pydantic import BaseModel

from pets.models import Ability, PetInstance


class Rival(BaseModel):
    name: str
    aliases: list[str]
    pets: tuple[PetInstance, PetInstance, PetInstance]


class BattleEvent(BaseModel):
    round: int
    actor: PetInstance
    target: PetInstance
    ability: Ability


class BattleLog(BaseModel):
    events: list[BattleEvent] = []

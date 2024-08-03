from pydantic import BaseModel

from pets.models import Pet


class Rival(BaseModel):
    name: str
    aliases: list[str]
    pets: tuple[Pet, Pet, Pet]

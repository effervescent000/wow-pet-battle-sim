from pydantic import BaseModel

from pets import models as pet_models


class Rival(BaseModel):
    name: str
    aliases: list[str]
    pets: tuple[pet_models.PetInstance, pet_models.PetInstance, pet_models.PetInstance]

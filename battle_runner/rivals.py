from battle_runner.battle_models import Rival, RivalPet
from pets.models import Stats


rivals: list[Rival] = [
    Rival(
        name="Haniko",
        pets=(
            RivalPet(
                name="Bloodbiter",
                family="Dragonkin",
                quality="Rare",
                abilities=["Bite", "Fade", "Proto-Strike"],
                stats=Stats(health=1319, power=309, speed=276),
            ),
            RivalPet(
                name="Faceripper",
                family="Dragonkin",
                quality="Rare",
                abilities=["Bite", "Feign Death", "Proto-Strike"],
                stats=Stats(health=1684, power=317, speed=195),
            ),
            RivalPet(
                name="Tina",
                family="Dragonkin",
                quality="Rare",
                abilities=["Emerald Bite", "Death Grip", "Starfall"],
                stats=Stats(health=1969, power=309, speed=358),
            ),
        ),
    )
]

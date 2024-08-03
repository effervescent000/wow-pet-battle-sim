from pet_reader.pet_reader import PetReader
from pets.db import PetDB


db = PetDB()
reader = PetReader(db)
reader.read_pets()

for pet in db.pets:
    print(pet)

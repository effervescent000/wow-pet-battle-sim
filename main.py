import argparse

from pet_reader.pet_reader import PetReader
from pets.db import PetDB
from team_builder.team_builder import TeamBuilder


db = PetDB()
reader = PetReader(db)
reader.read_pets()

parser = argparse.ArgumentParser(
    description="Find combination of pets to beat a given enemy"
)
parser.add_argument("-f", "--family", dest="family")
args = parser.parse_args()
team_builder = TeamBuilder(db, args.family)
team = team_builder.build_team()
print(team)

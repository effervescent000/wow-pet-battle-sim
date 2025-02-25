import pytest
from pet_reader.helpers import row_is_valid
from pet_reader.pet_reader import PetReader
from pets.db import PetDB


def test_parse_collection_values():
    db = PetDB()
    reader = PetReader(db)
    rows = [
        (
            "1",
            "Mana Wyrmling",
            "link",
            1,
            "Uncommon",
            "PB",
            "Magic",
            0,
            "Yes",
            "Yes",
            "Feedback",
            "Drain Power",
            "Mana Surge",
            "Flurry",
            "Amplify Magic",
            "Deflection",
            "8",
            "8",
            "8",
            "BB,HP,PB,HB",
            "136",
            "Vendor",
            "3",
            "Uncommon",
            "Yes",
            "Yes",
            "Burning Crusade",
            None,
            None,
            "88.18%",
            "6",
        ),
        (
            "1692",
            "Pocopoc",
            "link",
            "-",
            None,
            "-",
            "Magic",
            None,
            "No",
            "No",
            None,
            None,
            None,
            None,
            None,
            None,
            "8",
            "8",
            "8",
            "BB",
            "3247",
            "Vendor",
            "3",
            "Rare",
            "No",
            "Yes",
            "Shadowlands",
            None,
            None,
            "40.34%",
            "0",
        ),
    ]
    assert len(reader._parse_collection_values(rows)) == 1


@pytest.mark.parametrize(
    "given, expected, should",
    [
        (
            (
                "1732",
                "Groundshaker",
                "link",
                "-",
                None,
                "-",
                "Beast",
                None,
                "Yes",
                "No",
                "Horn Gore",
                "Headbutt",
                "Primal Cry",
                "Zap",
                "Lightning Shield",
                "Stampede",
                "8.375",
                "7.875",
                "7.75",
                "N/A",
                "3314",
                "Vendor",
                "Unknown",
                "Unknown",
                "Yes",
                "Yes",
                "Dragonflight",
                None,
                None,
                "0.00%",
                "0",
            ),
            False,
            "Unknown values should fail",
        ),
        (
            (
                "1728",
                "Trub'ul",
                "link",
                "-",
                None,
                "-",
                "Beast",
                None,
                "No",
                "No",
                None,
                None,
                None,
                None,
                None,
                None,
                "7.825",
                "8.675",
                "7.5",
                "N/A",
                "3188",
                None,
                "Unknown",
                "Unknown",
                "Yes",
                "Yes",
                "Dragonflight",
                None,
                None,
                "0.00%",
                "0",
            ),
            False,
            "Battle pets with no abilities should fail",
        ),
    ],
)
def test_row_is_valid(given, expected, should) -> None:
    result = row_is_valid(given)
    assert result == expected, should

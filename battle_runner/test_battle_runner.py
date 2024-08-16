from battle_runner.battle_runner import BattleRunner
from pets.shapes import pet_factory, pet_species_factory
from testing.world import AbilityLookup


def test_do_round_basic() -> None:
    """If both pets have done their moves with the default basic moveset,
    each pet should have < 100 health."""
    runner = BattleRunner(
        player_pets=(pet_factory(),),
        rival_pets=(pet_factory(),),
    )
    runner.do_round()
    assert runner.round == 1
    assert runner.player_pets[0].cur_health < 100
    assert runner.rival_pets[0].cur_health < 100


def test_effects_applied() -> None:
    """Modifiers are applied correctly."""
    runner = BattleRunner(
        player_pets=(
            pet_factory(
                species=pet_species_factory(abilities=["FakeTestWithBuffToOverwrite"])
            ),
        ),
        rival_pets=(pet_factory(),),
    )
    runner.do_round()
    assert len(runner.player_pets[0].modifiers) == 1
    assert runner.player_pets[0].modifiers[0].name == "Test Buff"
    assert runner.player_pets[0].modifiers[0].duration == 3
    assert len(runner.rival_pets[0].modifiers) == 0

    # can we overwrite the buff?
    runner.do_round()
    assert len(runner.player_pets[0].modifiers) == 1
    assert runner.player_pets[0].modifiers[0].duration == 3


def test_pet_ability_logic_with_conditions() -> None:
    runner = BattleRunner(
        player_pets=(
            pet_factory(species=pet_species_factory(abilities=["FakeTestWithBuff"])),
        ),
        rival_pets=(pet_factory(),),
    )
    runner.do_round()
    # should choose claw, because the buff is already applied
    assert runner.player_pets[0].select_ability(runner.rival_pets[0])[
        0
    ] == AbilityLookup.get("Claw")

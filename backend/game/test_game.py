from django.test import TestCase
from hypothesis import assume, given, strategies as st
import pytest

from game import models


def test_validation_wrapper():
    behavior = models.AdditiveBehavior(power=1, splash=5, radius=2)
    assert behavior.power == 1
    assert behavior.splash == 5
    assert behavior.radius == 2


@given(
    power=st.integers(max_value=10),
    splash=st.integers(max_value=10),
    radius=st.integers(max_value=10)
)
def test_validation_wrapper_invalid_inputs(power, splash, radius):
    # Skip conditions where all values are within limits
    for attribute, value in zip(["power", "splash", "radius"], [power, splash, radius]):
        allowable_range = models.AdditiveBehavior.allowable_values[attribute]
        if value in allowable_range:
            assume(False)

    with pytest.raises(ValueError) as e_info:
        models.AdditiveBehavior(power=power, splash=splash, radius=radius)

    for attribute, value in zip(["power", "splash", "radius"], [power, splash, radius]):
        allowable_range = models.AdditiveBehavior.allowable_values[attribute]
        if value not in allowable_range:
            error_msg = (
                f"{attribute.capitalize()} must be an integer "
                f"between {min(allowable_range)} and {max(allowable_range)}, inclusive"
            )
            assert error_msg in str(e_info.value)


def test_inclusive_range(start: int=1, stop: int=10):
    exclusive_range = range(start, stop)
    inclusive_range = models._inclusive_range(start, stop)
    assert min(inclusive_range) == min(exclusive_range)
    assert max(inclusive_range) == max(exclusive_range) + 1


@pytest.mark.parametrize("power,splash,radius", [(1, 3, 4)])
def test_additive_behavior_initialization(power, splash, radius):
    behavior = models.AdditiveBehavior(power=power, splash=splash, radius=radius)
    assert behavior.power == power
    assert behavior.splash == splash
    assert behavior.radius == radius


@pytest.mark.parametrize("power,range,rate", [(1, 3, 4)])
def test_multiplicative_behavior_initialization(power, range, rate):
    behavior = models.MultiplicativeBehavior(power=power, range=range, rate=rate)
    assert behavior.power == power
    assert behavior.range == range
    assert behavior.rate == rate


@pytest.mark.parametrize("id,cards", [(1, {})])
def test_tower_initialization(id, cards):
    tower = models.Tower(id=id, cards=cards)
    assert tower.id == id
    assert tower.cards == cards
    assert tower.tier == 1  # Default value


@pytest.mark.parametrize("power,splash,radius", [(1, 3, 4), (2, 2, 2), (3, 1, 1)])
def test_additive_behaviors_are_equal_for_same_inputs(power, splash, radius):
    card1 = models.AdditiveBehavior(power=power, splash=splash, radius=radius)
    card2 = models.AdditiveBehavior(power=power, splash=splash, radius=radius)
    assert card1 == card2


def test_additive_behaviors_are_not_equal_for_different_inputs():
    card1 = models.AdditiveBehavior(power=1, splash=1, radius=1)
    card2 = models.AdditiveBehavior(power=1, splash=2, radius=1)
    assert not card1 == card2


@pytest.mark.parametrize("power,range,rate", [(1, 3, 4), (2, 2, 2), (3, 1, 1)])
def test_multiplicative_behaviors_are_equal_for_same_inputs(power, range, rate):
    card1 = models.MultiplicativeBehavior(power=power, range=range, rate=rate)
    card2 = models.MultiplicativeBehavior(power=power, range=range, rate=rate)
    assert card1 == card2


def test_multiplicative_behaviors_are_not_equal_for_different_inputs():
    card1 = models.MultiplicativeBehavior(power=1, range=1, rate=1)
    card2 = models.MultiplicativeBehavior(power=1, range=2, rate=1)
    assert not card1 == card2


def test_behaviors_of_differing_types_are_not_equal():
    card1 = models.AdditiveBehavior(power=1, splash=1, radius=1)
    card2 = models.MultiplicativeBehavior(power=1, range=1, rate=1)
    assert not card1 == card2

    card1 = models.MultiplicativeBehavior(power=1, range=1, rate=1)
    card2 = models.AdditiveBehavior(power=1, splash=1, radius=1)
    assert not card1 == card2


def test_tower_with_same_cards_in_same_order_are_equal():
    card1 = models.MultiplicativeBehavior(power=1, range=1, rate=1)
    card2 = models.AdditiveBehavior(power=1, splash=1, radius=1)
    tower1 = models.Tower(id=1, cards={1: card1, 2: card2})
    tower2 = models.Tower(id=1, cards={1: card1, 2: card2})
    assert tower1 == tower2


def test_tower_with_same_cards_in_different_order_are_not_equal():
    card1 = models.MultiplicativeBehavior(power=1, range=1, rate=1)
    card2 = models.AdditiveBehavior(power=1, splash=1, radius=1)
    tower1 = models.Tower(id=1, cards={1: card1, 2: card2})
    tower2 = models.Tower(id=1, cards={1: card2, 2: card1})
    assert not tower1 == tower2


def test_tower_is_not_equal_to_non_tower_object():
    tower = models.Tower(id=1, cards={})
    assert not tower == 1


def test_tower_initialization_beyond_tier_limit_failure():
    max_tier = max(models.Tower.allowable_values["tier"])
    with pytest.raises(ValueError):
        tower = models.Tower(id=1, cards={}, tier= max_tier + 1)


def test_tower_upgrade_beyond_tier_limit_failure():
    tower = models.Tower(id=1, cards={}, tier=1)
    max_tier = max(models.Tower.allowable_values["tier"])
    with pytest.raises(ValueError):
        tower.tier = max_tier + 1


def test_tower_upgrade_within_limit_success():
    tower = models.Tower(id=1, cards={}, tier=1)
    max_tier = max(models.Tower.allowable_values["tier"])
    tower.tier = max_tier
    assert tower.tier == max_tier


def test_tower_level_up_below_max_level_success():
    max_tier = max(models.Tower.allowable_values["tier"])
    tower = models.Tower(id=1, cards={}, tier=max_tier - 1)
    tower.level_up()
    assert tower.tier == max_tier


def test_tower_level_up_at_max_level_failure():
    max_tier = max(models.Tower.allowable_values["tier"])
    tower = models.Tower(id=1, cards={}, tier=max_tier)
    with pytest.raises(ValueError):
        tower.level_up()

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


def test_additive_behavior_initialization(
        power: int=1,
        splash: int=3,
        radius: int=4
):
    behavior = models.AdditiveBehavior(power=power, splash=splash, radius=radius)
    assert behavior.power == power
    assert behavior.splash == splash
    assert behavior.radius == radius


def test_multiplicative_behavior_initialization(
        power: int=1,
        range: int=3,
        rate: int=4
):
    behavior = models.MultiplicativeBehavior(power=power, range=range, rate=rate)
    assert behavior.power == power
    assert behavior.range == range
    assert behavior.rate == rate


def test_tower_initialization():
    tower = models.Tower(id=id, cards={})
    assert tower.id == id
    assert tower.cards == {}


# def test_tower_with_same_cards_are_equal():

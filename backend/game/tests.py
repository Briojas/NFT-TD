from django.test import TestCase
from hypothesis import given, strategies as st
import pytest

from game import models


def test_validation_wrapper():
    card = models.Card(tier=2, priority=5)
    assert card.tier == 2
    assert card.priority == 5


def test_validation_wrapper_invalid_inputs():
    with pytest.raises(ValueError) as e_info:
        card = models.Card(tier=5, priority=5)
    assert "Tier must be an integer between 1 and 3, inclusive" in str(e_info.value)


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


@given(
    tier=st.integers(min_value=1, max_value=3),
    priority=st.integers(min_value=1, max_value=7)
)
def test_card_initialization(tier, priority):
    """Tests card with an additive operator (+/-)

    Requirements:
    - Additive card has three attributes:
       - tier (int): Value from 1 to 3
       - priority (int): Value from 1 to 7
       - behavior (Behavior): Custom class
    """
    card = models.Card(tier=tier, priority=priority, behavior=None)
    assert card.tier == tier
    assert card.priority == priority

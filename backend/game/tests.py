from django.test import TestCase
from hypothesis import given, strategies as st

from game import models


def test_inclusive_range(start=1, stop=10):
    exclusive_range = range(start, stop)
    inclusive_range = models._inclusive_range(start, stop)
    assert min(inclusive_range) == min(exclusive_range)
    assert max(inclusive_range) == max(exclusive_range) + 1


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

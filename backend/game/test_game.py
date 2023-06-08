from django.test import TestCase
from hypothesis import assume, given, strategies as st
import pytest

from game import models


@pytest.fixture
def tech_tree_cards():
    return {
            'Top1': 'Top1 card',
            'Top2': 'Top2 card',
            'Mid1': 'Mid1 card',
            'Mid2': 'Mid2 card',
            'Mid3': 'Mid3 card',
            'Bot1': 'Bot1 card',
            'Bot2': 'Bot2 card'
    }


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


def test_tower_initialization(tech_tree_cards):
    tower = models.Tower(tech_tree=tech_tree_cards)
    assert isinstance(tower.tech_tree, models.TechTree)
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


def test_tech_tree_initialization(tech_tree_cards):
    tech_tree = models.TechTree(cards=tech_tree_cards)

    for name in ['Top1', 'Top2', 'Mid1', 'Mid2', 'Mid3', 'Bot1', 'Bot2']:
        assert name in tech_tree.cards

    assert tech_tree.cards['Top1']['prerequisites'] == set()
    assert tech_tree.cards['Top2']['prerequisites'] == set()
    assert tech_tree.cards['Mid1']['prerequisites'] == set(['Top1'])
    assert tech_tree.cards['Mid2']['prerequisites'] == set(['Top1', 'Top2'])
    assert tech_tree.cards['Mid3']['prerequisites'] == set(['Top2'])
    assert tech_tree.cards['Bot1']['prerequisites'] == set(['Mid1', 'Mid2'])
    assert tech_tree.cards['Bot2']['prerequisites'] == set(['Mid2', 'Mid3'])


def test_tech_tree_node_is_unlockable(tech_tree_cards):
    tech_tree = models.TechTree(cards=tech_tree_cards)

    assert tech_tree.is_unlockable('Top1', unlocked_cards=[]) == True
    assert tech_tree.is_unlockable('Bot2', unlocked_cards=[]) == False
    assert tech_tree.is_unlockable('Bot2', unlocked_cards=['Top1', 'Mid2']) == True


def test_identical_tech_tree_is_equal(tech_tree_cards):
    tree1 = models.TechTree(cards=tech_tree_cards)
    tree2 = models.TechTree(cards=tech_tree_cards)
    assert tree1 == tree2


def test_tower_with_same_tech_tree_are_equal(tech_tree_cards):
    tower1 = models.Tower(tech_tree=tech_tree_cards, tier=2)
    tower2 = models.Tower(tech_tree=tech_tree_cards, tier=2)
    assert tower1 == tower2


def test_tower_is_not_equal_to_non_tower_object(tech_tree_cards):
    tower = models.Tower(tech_tree=tech_tree_cards)
    assert not tower == 1


def test_tower_initialization_beyond_tier_limit_failure(tech_tree_cards):
    max_tier = max(models.Tower.allowable_values["tier"])
    with pytest.raises(ValueError):
        tower = models.Tower(tech_tree=tech_tree_cards, tier= max_tier + 1)


def test_tower_upgrade_beyond_tier_limit_failure(tech_tree_cards):
    tower = models.Tower(tech_tree=tech_tree_cards, tier=1)
    max_tier = max(models.Tower.allowable_values["tier"])
    with pytest.raises(ValueError):
        tower.tier = max_tier + 1


def test_tower_upgrade_within_limit_success(tech_tree_cards):
    tower = models.Tower(tech_tree=tech_tree_cards, tier=1)
    max_tier = max(models.Tower.allowable_values["tier"])
    tower.tier = max_tier
    assert tower.tier == max_tier


def test_tower_level_up_below_max_level_success(tech_tree_cards):
    max_tier = max(models.Tower.allowable_values["tier"])
    tower = models.Tower(tech_tree=tech_tree_cards, tier=max_tier - 1)
    tower.level_up()
    assert tower.tier == max_tier


def test_tower_level_up_at_max_level_failure(tech_tree_cards):
    max_tier = max(models.Tower.allowable_values["tier"])
    tower = models.Tower(tech_tree=tech_tree_cards, tier=max_tier)
    with pytest.raises(ValueError):
        tower.level_up()

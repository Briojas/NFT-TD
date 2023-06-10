from django.core.exceptions import ValidationError
from django.test import TestCase
from game import models


def test_inclusive_range(start: int=1, stop: int=10):
    exclusive_range = range(start, stop)
    inclusive_range = models._inclusive_range(start, stop)
    assert min(inclusive_range) == min(exclusive_range)
    assert max(inclusive_range) == max(exclusive_range) + 1


class TestAdditiveBehavior(TestCase):
    def setUp(self):
        self.power = 1
        self.splash = 5
        self.radius = 2
        self.behavior = models.AdditiveBehavior(
            power=self.power,
            splash=self.splash,
            radius=self.radius
        )

    def test_initialization(self):
        self.assertEqual(self.behavior.power, self.power)
        self.assertEqual(self.behavior.splash, self.splash)
        self.assertEqual(self.behavior.radius, self.radius)

    def test_behaviors_are_equal_for_same_inputs(self):
        self.behavior_with_same_inputs = models.AdditiveBehavior(
            power=self.power, splash=self.splash, radius=self.radius
        )
        self.assertEqual(self.behavior, self.behavior_with_same_inputs)

    def test_behaviors_are_not_equal_for_different_inputs(self):
        self.behavior_with_different_inputs = models.AdditiveBehavior(
            power=self.power + 1, splash=self.splash, radius=self.radius
        )
        self.assertNotEqual(self.behavior, self.behavior_with_different_inputs)

    def test_behaviors_of_differing_types_are_not_equal(self):
        self.behavior_of_different_type = models.MultiplicativeBehavior(
            power=self.power, range=self.splash, rate=self.radius
        )
        self.assertNotEqual(self.behavior, self.behavior_of_different_type)


class TestMultiplicativeBehavior(TestCase):
    def setUp(self):
        self.power = 1
        self.range = 3
        self.rate = 4
        self.behavior = models.MultiplicativeBehavior(
            power=self.power,
            range=self.range,
            rate=self.rate
        )

    def test_initialization(self):
        self.assertEqual(self.behavior.power, self.power)
        self.assertEqual(self.behavior.range, self.range)
        self.assertEqual(self.behavior.rate, self.rate)

    def test_behaviors_are_equal_for_same_inputs(self):
        self.behavior_with_same_inputs = models.MultiplicativeBehavior(
            power=self.power, range=self.range, rate=self.rate
        )
        self.assertEqual(self.behavior, self.behavior_with_same_inputs)

    def test_behaviors_are_not_equal_for_different_inputs(self):
        self.behavior_with_different_inputs = models.MultiplicativeBehavior(
            power=self.power + 1, range=self.range, rate=self.rate
        )
        self.assertNotEqual(self.behavior, self. behavior_with_different_inputs)

    def test_behaviors_of_differing_types_are_not_equal(self):
        self.behavior_of_different_type = models.AdditiveBehavior(power=1, splash=1, radius=1)
        self.assertNotEqual(self.behavior, self.behavior_of_different_type)


class TestTechTree(TestCase):
    def setUp(self):
        self.cards = {
            'Top1': 'Top1',
            'Top2': 'Top2',
            'Mid1': 'Mid1',
            'Mid2': 'Mid2',
            'Mid3': 'Mid3',
            'Bot1': 'Bot1',
            'Bot2': 'Bot2',
        }
        self.tech_tree = models.TechTree.create(cards=self.cards)

    def test_initialization(self):
        for name in ['Top1', 'Top2', 'Mid1', 'Mid2', 'Mid3', 'Bot1', 'Bot2']:
            self.assertIn(name, self.tech_tree.cards)

        self.assertEqual(self.tech_tree.cards['Top1']['prerequisites'], list())
        self.assertEqual(self.tech_tree.cards['Top2']['prerequisites'], list())
        self.assertEqual(self.tech_tree.cards['Mid1']['prerequisites'], list(['Top1']))
        self.assertEqual(self.tech_tree.cards['Mid2']['prerequisites'], list(['Top1', 'Top2']))
        self.assertEqual(self.tech_tree.cards['Mid3']['prerequisites'], list(['Top2']))
        self.assertEqual(self.tech_tree.cards['Bot1']['prerequisites'], list(['Mid1', 'Mid2']))
        self.assertEqual(self.tech_tree.cards['Bot2']['prerequisites'], list(['Mid2', 'Mid3']))

    def test_node_is_unlockable(self):
        self.assertTrue(self.tech_tree.is_unlockable('Top1', unlocked_cards=[]))
        self.assertFalse(self.tech_tree.is_unlockable('Bot2', unlocked_cards=[]))
        self.assertTrue(self.tech_tree.is_unlockable('Bot2', unlocked_cards=['Top1', 'Mid2']))

    def test_identical_trees_are_equal(self):
        tree2 = models.TechTree.create(cards=self.cards)
        self.assertEqual(self.tech_tree, tree2)


class TestTower(TestCase):
    def setUp(self):
        self.tech_tree_cards = {
            'Top1': 'Top1 card',
            'Top2': 'Top2 card',
            'Mid1': 'Mid1 card',
            'Mid2': 'Mid2 card',
            'Mid3': 'Mid3 card',
            'Bot1': 'Bot1 card',
            'Bot2': 'Bot2 card'
        }
        self.tech_tree = models.TechTree.create(cards=self.tech_tree_cards)
        self.tech_tree.save()
        self.tower = models.Tower(tech_tree=self.tech_tree)
        self.max_tier = max(choice[0] for choice in models.Tower.TIER_CHOICES)

    def test_initialization(self):
        self.assertIsInstance(self.tower.tech_tree, models.TechTree)
        self.assertEqual(self.tower.tier, 1)

    def test_towers_with_same_tech_tree_are_equal(self):
        tower2 = models.Tower(tech_tree=self.tech_tree, tier=2)
        self.assertEqual(self.tower, tower2)

    def test_tower_is_not_equal_to_non_tower_object(self):
        self.assertNotEqual(self.tower, 1)
        self.assertNotEqual(self.tower, "string")
        self.assertNotEqual(self.tower, [])
        self.assertNotEqual(self.tower, {})
        self.assertNotEqual(self.tower, models.TechTree(cards=self.tech_tree_cards))

    def test_saving_tower_with_tier_beyond_limit_raises_error(self):
        self.tower.tier = self.max_tier + 1
        with self.assertRaises(ValidationError):
            self.tower.save()

    def test_saving_tower_with_tier_within_limit_success(self):
        self.tower.tier = self.max_tier
        self.tower.save()
        self.assertEqual(self.tower.tier, self.max_tier)

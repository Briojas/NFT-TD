"""This module contains the building blocks for a math-based tower defense game

"""

from django.db import models


def _inclusive_range(start: int, stop: int):
    return range(start, stop + 1)


class AdditiveBehavior(models.Model):
    POWER_CHOICES = [(i, i) for i in _inclusive_range(1, 3)]
    SPLASH_CHOICES = [(i, i) for i in _inclusive_range(1, 7)]
    RADIUS_CHOICES = [(i, i) for i in _inclusive_range(1, 10)]

    power = models.IntegerField(choices=POWER_CHOICES)
    splash = models.IntegerField(choices=SPLASH_CHOICES)
    radius = models.IntegerField(choices=RADIUS_CHOICES)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.power == other.power and
                self.splash == other.splash and
                self.radius == other.radius
            )
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class MultiplicativeBehavior(models.Model):
    POWER_CHOICES = [(i, i) for i in _inclusive_range(1, 3)]
    RANGE_CHOICES = [(i, i) for i in _inclusive_range(1, 7)]
    RATE_CHOICES = [(i, i) for i in _inclusive_range(1, 10)]

    power = models.IntegerField(choices=POWER_CHOICES)
    range = models.IntegerField(choices=RANGE_CHOICES)
    rate = models.IntegerField(choices=RATE_CHOICES)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
                self.power == other.power and
                self.range == other.range and
                self.rate == other.rate
            )
        return False

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class TechTree(models.Model):
    cards = models.JSONField()

    @classmethod
    def create(cls, cards):
        tech_tree = cls()
        tech_tree.cards = {}

        # Add cards to the tree
        for card_name, card in cards.items():
            tech_tree.add_card(card_name, card)

        # Set prerequisites
        tech_tree.add_prerequisite('Mid1', prerequisite='Top1')
        tech_tree.add_prerequisite('Mid2', prerequisite='Top1')
        tech_tree.add_prerequisite('Mid2', prerequisite='Top2')
        tech_tree.add_prerequisite('Mid3', prerequisite='Top2')
        tech_tree.add_prerequisite('Bot1', prerequisite='Mid1')
        tech_tree.add_prerequisite('Bot1', prerequisite='Mid2')
        tech_tree.add_prerequisite('Bot2', prerequisite='Mid2')
        tech_tree.add_prerequisite('Bot2', prerequisite='Mid3')

        return tech_tree

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.cards == other.cards
        return False  # pragma: no cover

    def add_card(self, card_name, card):
        # Add a card with no prerequisites
        if card_name not in self.cards:
            self.cards[card_name] = {'card': card, 'prerequisites': set()}

    def add_prerequisite(self, card_name, prerequisite):
        # Add the prerequisite to the prerequisites for the card
        if prerequisite not in self.cards[card_name]['prerequisites']:
            self.cards[card_name]['prerequisites'].add(prerequisite)

    def is_unlockable(self, card_name, unlocked_cards):
        # Returns true if any of the prerequisites for the card are in the list of unlocked cards
        prereqs = self.cards[card_name]['prerequisites']
        if prereqs:
            intersection = prereqs.intersection(set(unlocked_cards))
        else:
            return True
        return bool(intersection)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Tower(models.Model):
    TIER_CHOICES = [(i,i) for i in _inclusive_range(1, 3)]

    tech_tree = models.ForeignKey(TechTree, on_delete=models.CASCADE)
    tier = models.IntegerField(choices=TIER_CHOICES, default=1)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.tech_tree == other.tech_tree
        return False  # pragma: no cover

    def level_up(self):
        self.tier += 1
        # At this point, a card may be added to the tower

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

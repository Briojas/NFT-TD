"""This module contains the building blocks for a math-based tower defense game

"""

from django.db import models
from typing import get_type_hints
import inspect


def _inclusive_range(start: int, stop: int):
    return range(start, stop + 1)


def _validate_inputs_setter(func):
    def wrapper(self, value):
        param_name = func.__name__
        allowed_values = self.allowable_values.get(param_name, None)
        if value not in allowed_values:
            raise ValueError(f"The input value for {param_name} is not valid.")
        return func(self, value)
    return wrapper


def _validate_inputs(func):
    sig = inspect.signature(func)

    def wrapper(self, *args, **kwargs):
        # bind the function arguments to their names
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()

        errors = []
        type_hints = get_type_hints(func)

        for attribute, value in bound_args.arguments.items():
            if attribute == "self":
                continue

            allowable_range = self.allowable_values.get(attribute)
            expected_type = type_hints.get(attribute)

            if allowable_range is None or expected_type is None:
                continue

            if not isinstance(value, expected_type) or value not in allowable_range:
                min_allowable = min(allowable_range)
                max_allowable = max(allowable_range)
                errors.append(
                    f"{attribute.capitalize()} must be an integer between {min_allowable} and {max_allowable}, inclusive"
                )

        if errors:
            raise ValueError('Invalid input(s):\n' + '\n'.join(errors))

        return func(self, *args, **kwargs)

    return wrapper


class AdditiveBehavior:
    allowable_values = {
        'power': _inclusive_range(1, 3),
        'splash': _inclusive_range(1, 7),
        'radius': _inclusive_range(1, 10)
    }

    @_validate_inputs
    def __init__(self, power: int, splash: int, radius: int):
        self.power = power
        self.splash = splash
        self.radius = radius

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return vars(self) == vars(other)
        return False


class MultiplicativeBehavior:
    allowable_values = {
        'power': _inclusive_range(1, 3),
        'range': _inclusive_range(1, 7),
        'rate': _inclusive_range(1, 10)
    }

    @_validate_inputs
    def __init__(self, power: int, range: int, rate: int):
        self.power = power
        self.range = range
        self.rate = rate

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return vars(self) == vars(other)
        return False


class Tower:
    allowable_values = {
        'tier': _inclusive_range(1, 3)
    }

    @_validate_inputs
    def __init__(self, tech_tree, unlocked_cards: set=None, tier: int=1):
        """Initialize a Tower instance

        Args:
            tech_tree (TechTree): A tech tree defining cards and their
                                  prerequisites
            tier (int, optional): The "level" of the tower
                                  Default 1. Max 3.
        """
        self.tech_tree = TechTree(tech_tree)
        self.unlocked_cards = unlocked_cards if unlocked_cards else set()
        self._tier = tier

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.tech_tree == other.tech_tree
        return False  # pragma: no cover

    @property
    def tier(self):
        return self._tier

    @tier.setter
    @_validate_inputs_setter
    def tier(self, tier):
        self._tier = tier

    def level_up(self):
        self.tier += 1
        # At this point, a card may be added to the tower


class TechTree:
    def __init__(self, cards):
        self.cards = {}
        
        # Add cards to the tree
        for card_name, card in cards.items():
            self.add_card(card_name, card)

        # Set prerequisites
        self.add_prerequisite('Mid1', prerequisite='Top1')
        self.add_prerequisite('Mid2', prerequisite='Top1')
        self.add_prerequisite('Mid2', prerequisite='Top2')
        self.add_prerequisite('Mid3', prerequisite='Top2')
        self.add_prerequisite('Bot1', prerequisite='Mid1')
        self.add_prerequisite('Bot1', prerequisite='Mid2')
        self.add_prerequisite('Bot2', prerequisite='Mid2')
        self.add_prerequisite('Bot2', prerequisite='Mid3')

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

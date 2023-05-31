"""This module contains the building blocks for a math-based tower defense game

"""

from django.db import models
from typing import get_type_hints


def _inclusive_range(start: int, stop: int):
    return range(start, stop + 1)


def _validate_inputs(func):
    def wrapper(self, **kwargs):
        errors = []
        type_hints = get_type_hints(func)

        for attribute, allowable_range in self.allowable_values.items():
            value = kwargs.get(attribute)
            expected_type = type_hints.get(attribute)
            if not isinstance(value, expected_type) or value not in allowable_range:
                min_allowable = min(allowable_range)
                max_allowable = max(allowable_range)
                errors.append(
                    f"{attribute.capitalize()} must be an integer between {min_allowable} and {max_allowable}, inclusive"
                )

        if errors:
            raise ValueError('Invalid input(s):\n' + '\n'.join(errors))

        return func(self, **kwargs)

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
    def __init__(self, id: int, cards: dict):
        self.id = id
        # Ensure stored cards are sorted by priority
        self.cards = {k: v for k, v in sorted(cards.items())}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.cards == other.cards
        return False  # pragma: no cover

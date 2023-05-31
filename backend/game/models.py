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


class TooManyCardsError(ValueError):
    def __init__(self, message=None, extra_info=None):
        if message is None:
            message = "The number of cards may not exceed the tower's tier"
        super().__init__(message)
        self.extra_info = extra_info


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
    def __init__(self, id: int, cards: dict, tier: int=1):
        """Initialize a Tower instance

        Args:
            id (int): _description_
            cards (dict): A dictionary of the towers behavior cards.
              The number of cards allowed corresponds to the tier of the tower.
              The order of the dictionary prioritizes the logical firing order
              for the behaviors.

              Ex: cards = {
                   1: card1,  # This card will be the first to be applied
                   2: card2   # This card will be the second to be applied
              }
            tier (int, optional): The "level" of the tower. Defaults to 1. Max 3.
        """
        if len(cards) > tier:
            raise TooManyCardsError

        self.id = id
        # Ensure stored cards are sorted
        self._cards = {k: v for k, v in sorted(cards.items())}
        self._tier = tier

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.cards == other.cards
        return False  # pragma: no cover

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, cards):
        if len(cards) > self.tier:
            raise TooManyCardsError
        # Ensure stored cards are sorted
        self._cards = {k: v for k, v in sorted(cards.items())}

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

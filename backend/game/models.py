"""This module contains the building blocks for a math-based tower defense game

"""

from django.db import models


def _inclusive_range(start: int, stop: int):
    return range(start, stop + 1)


class Card:
    allowable_tier_range = _inclusive_range(1, 3)
    allowable_priority_range = _inclusive_range(1, 7)

    def __init__(self, tier: int, priority: int, behavior=None):
        errors = []
        if not isinstance(tier, int) or tier not in Card.allowable_tier_range:
            min_allowable = min(Card.allowable_tier_range)
            max_allowable = max(Card.allowable_tier_range)
            errors.append(
                f"Tier must be an integer between {min_allowable} and {max_allowable}, inclusive"
            )
        if not isinstance(priority, int) or priority not in Card.allowable_priority_range:
            min_allowable = min(Card.allowable_priority_range)
            max_allowable = max(Card.allowable_priority_range)
            errors.append(
                f"Priority must be an integer between {min_allowable} and {max_allowable}, inclusive"
            )

        if errors:
            raise ValueError('Invalid input(s):\n' + '\n'.join(errors))

        self.tier = tier
        self.priority = priority
        self.behavior = behavior

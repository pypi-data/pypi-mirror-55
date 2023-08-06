"""Utilities for dealing with optional values."""

import typing as t


def exists(value: t.Any) -> bool:
    """Return whether the value is not None.

    This is useful to differentiate between Falsey values and None
    without having to resort to the `is [not] None` comparison. In
    addition, it composes nicely with filter.

    >>> assert exists(None) is False
    >>> assert exists([]) is True
    >>> assert tuple(filter(exists, (1, 2, None))) == (1, 2)
    """
    return value is not None

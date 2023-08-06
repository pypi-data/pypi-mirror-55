"""Utilities for easier iteration."""

import typing as t
from itertools import islice


T = t.TypeVar("T")
U = t.TypeVar("U")


def first(items: t.Iterable[T]) -> t.Optional[T]:
    """Return the first item from items, or None.

    >>> assert first(range(10)) == 0
    >>> assert first(()) is None
    """
    just_first = tuple(take(1, items))
    return None if len(just_first) == 0 else just_first[0]


def for_each(fn: t.Callable[[T], t.Any], items: t.Iterable[T]) -> None:
    """Call the function on each of the provided items.

    This is expected to be used for code with side effects and explicitly
    returns None.

    >>> collect = []
    >>> for_each(lambda i: collect.append(i), range(5))
    >>> assert collect == [0, 1, 2, 3, 4]
    """
    for i in items:
        fn(i)


def take(n: int, items: t.Iterable[T]) -> t.Iterator[T]:
    """Take up to `n` items from the provided iterable.

    >>> assert tuple(take(2, (1, 2, 3))) == (1, 2)
    >>> assert tuple(take(2, (1,))) == (1,)
    >>> assert tuple(take(2, ())) == ()
    """
    yield from islice(items, n)

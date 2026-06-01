from __future__ import annotations

from collections.abc import Callable, Iterable
from itertools import product


BinaryPoint = tuple[int, ...]
Predicate = Callable[[BinaryPoint], bool]


def enumerate_binary_points(
    dimension: int,
    predicate: Predicate | None = None,
) -> list[BinaryPoint]:
    """Enumerate binary points of a given dimension.

    This is intended for small computational experiments only.
    """
    if dimension < 0:
        raise ValueError("dimension must be nonnegative.")

    points = []

    for point in product((0, 1), repeat=dimension):
        if predicate is None or predicate(point):
            points.append(point)

    return points
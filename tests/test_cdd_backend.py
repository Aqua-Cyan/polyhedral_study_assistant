from fractions import Fraction

import pytest

from psa.inequality import LinearInequality


pytest.importorskip("cdd")


def test_unit_square_convex_hull_inequalities() -> None:
    from psa.backends.cdd import convex_hull_inequalities_from_points

    points = [
        [0, 0],
        [1, 0],
        [0, 1],
        [1, 1],
    ]

    inequalities = set(convex_hull_inequalities_from_points(points))

    expected = {
        LinearInequality((-1, 0), 0, "<=").normalized(),
        LinearInequality((0, -1), 0, "<=").normalized(),
        LinearInequality((1, 0), 1, "<=").normalized(),
        LinearInequality((0, 1), 1, "<=").normalized(),
    }

    assert inequalities == expected


def test_row_to_integer_values_clears_denominators() -> None:
    from psa.backends.cdd import _row_to_integer_values

    row = [Fraction(1, 2), Fraction(-3, 4), Fraction(5, 6)]

    assert _row_to_integer_values(row) == [6, -9, 10]


def test_row_to_integer_values_preserves_integers() -> None:
    from psa.backends.cdd import _row_to_integer_values

    assert _row_to_integer_values([1, -2, 3]) == [1, -2, 3]

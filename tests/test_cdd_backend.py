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
        LinearInequality((-1, 0), 0, "<=").normalized(),  # x1 >= 0
        LinearInequality((0, -1), 0, "<=").normalized(),  # x2 >= 0
        LinearInequality((1, 0), 1, "<=").normalized(),   # x1 <= 1
        LinearInequality((0, 1), 1, "<=").normalized(),   # x2 <= 1
    }

    assert inequalities == expected
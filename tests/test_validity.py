from psa.inequality import LinearInequality
from psa.validity import (
    check_validity_on_points,
    find_violating_point,
    satisfies_point,
)


def test_satisfies_point_for_less_equal() -> None:
    inequality = LinearInequality((1, 1), 1, "<=")

    assert satisfies_point(inequality, (1, 0))
    assert satisfies_point(inequality, (0, 1))
    assert not satisfies_point(inequality, (1, 1))


def test_find_violating_point() -> None:
    inequality = LinearInequality((1, 1), 1, "<=")
    points = [(0, 0), (1, 0), (1, 1)]

    result = find_violating_point(inequality, points)

    assert result is not None
    point, violation = result
    assert point == (1, 1)
    assert violation == 1


def test_check_validity_on_points_valid_case() -> None:
    inequality = LinearInequality((-1, 0), 0, "<=")  # x1 >= 0
    points = [(0, 0), (1, 0), (1, 1)]

    result = check_validity_on_points(inequality, points)

    assert result.is_valid
    assert result.violating_point is None
    assert result.checked_points == 3


def test_check_validity_on_points_invalid_case() -> None:
    inequality = LinearInequality((1, 1), 1, "<=")
    points = [(0, 0), (1, 0), (1, 1)]

    result = check_validity_on_points(inequality, points)

    assert not result.is_valid
    assert result.violating_point == (1, 1)
    assert result.violation_value == 1
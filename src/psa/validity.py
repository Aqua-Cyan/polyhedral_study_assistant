from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from psa.inequality import LinearInequality


Point = Sequence[int | float]


@dataclass(frozen=True)
class ValidityCheckResult:
    """Result of checking one inequality on a finite point set."""

    is_valid: bool
    checked_points: int
    violating_point: tuple[int | float, ...] | None = None
    violation_value: int | float | None = None
    message: str = ""


def lhs_value(inequality: LinearInequality, point: Point) -> int | float:
    """Evaluate the left-hand side of a LinearInequality at a point."""
    if len(inequality.coefficients) != len(point):
        raise ValueError(
            "Point dimension does not match inequality dimension: "
            f"{len(point)} != {len(inequality.coefficients)}."
        )

    return sum(coefficient * value for coefficient, value in zip(inequality.coefficients, point, strict=True))


def violation_value(inequality: LinearInequality, point: Point) -> int | float:
    """Return a positive value when the inequality is violated.

    For a <= inequality, this returns lhs - rhs.
    For a >= inequality, this returns rhs - lhs.
    For equality, this returns abs(lhs - rhs).
    """
    lhs = lhs_value(inequality, point)

    if inequality.sense == "<=":
        return lhs - inequality.rhs
    if inequality.sense == ">=":
        return inequality.rhs - lhs
    if inequality.sense == "=":
        return abs(lhs - inequality.rhs)

    raise ValueError(f"Unsupported inequality sense: {inequality.sense}")


def satisfies_point(
    inequality: LinearInequality,
    point: Point,
    *,
    tolerance: float = 0.0,
) -> bool:
    """Return whether a point satisfies an inequality."""
    return violation_value(inequality, point) <= tolerance


def find_violating_point(
    inequality: LinearInequality,
    points: Iterable[Point],
    *,
    tolerance: float = 0.0,
) -> tuple[tuple[int | float, ...], int | float] | None:
    """Find the first point violating an inequality.

    Returns
    -------
    None
        If no violating point is found.
    (point, violation)
        If a violating point is found.
    """
    for point in points:
        point_tuple = tuple(point)
        violation = violation_value(inequality, point_tuple)
        if violation > tolerance:
            return point_tuple, violation

    return None


def check_validity_on_points(
    inequality: LinearInequality,
    points: Iterable[Point],
    *,
    tolerance: float = 0.0,
) -> ValidityCheckResult:
    """Check whether an inequality is valid on a finite point set.

    This is not a proof of general validity. It is a finite validation gate
    for candidate symbolic families instantiated on small examples.
    """
    checked_points = 0

    for point in points:
        checked_points += 1
        point_tuple = tuple(point)
        violation = violation_value(inequality, point_tuple)
        if violation > tolerance:
            return ValidityCheckResult(
                is_valid=False,
                checked_points=checked_points,
                violating_point=point_tuple,
                violation_value=violation,
                message="A violating point was found.",
            )

    return ValidityCheckResult(
        is_valid=True,
        checked_points=checked_points,
        message="No violating point was found in the finite point set.",
    )


def check_all_equalities_against_points(
    inequalities: Iterable[LinearInequality],
    points: Iterable[Point],
    *,
    tolerance: float = 0.0,
) -> list[ValidityCheckResult]:
    """Check a collection of inequalities on the same finite point set."""
    point_list = [tuple(point) for point in points]
    return [
        check_validity_on_points(inequality, point_list, tolerance=tolerance)
        for inequality in inequalities
    ]
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol, Sequence

from psa.inequality import LinearInequality
from psa.validity import ValidityCheckResult, check_validity_on_points


@dataclass(frozen=True)
class FamilyParameter:
    """A concrete parameter assignment for a symbolic inequality family."""

    values: Mapping[str, object]

    def describe(self) -> str:
        return ", ".join(f"{key}={value!r}" for key, value in self.values.items())


@dataclass(frozen=True)
class FamilyInstantiation:
    """A concrete inequality obtained by instantiating a symbolic family."""

    family_name: str
    parameter: FamilyParameter
    inequality: LinearInequality
    derivation_status: str = "unknown"
    validity_status: str = "unchecked"
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class FamilyMatch:
    """An exact match between a family instantiation and a computed facet."""

    family_name: str
    parameter: FamilyParameter
    instantiated_inequality: LinearInequality
    computed_facet: LinearInequality
    status: str
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class InvalidatedFamilyInstance:
    """A family instantiation disproved by a finite feasible point."""

    family_name: str
    parameter: FamilyParameter
    inequality: LinearInequality
    violating_point: tuple[int | float, ...]
    violation_value: int | float
    source: str | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CandidateFamilyValidation:
    """Validation record for one candidate family instantiation."""

    instantiation: FamilyInstantiation
    finite_validity: ValidityCheckResult
    exact_matches: tuple[FamilyMatch, ...] = ()
    invalidation: InvalidatedFamilyInstance | None = None
    status: str = "unchecked"
    notes: tuple[str, ...] = ()


class InequalityFamilyProtocol(Protocol):
    """Protocol for symbolic inequality families.

    Problem-specific families should implement these two methods.
    """

    name: str

    def enumerate_parameters(self, instance: object) -> Sequence[FamilyParameter]:
        ...

    def instantiate(self, instance: object, parameter: FamilyParameter) -> LinearInequality:
        ...


def normalized_equal(lhs: LinearInequality, rhs: LinearInequality) -> bool:
    """Return whether two inequalities are equal after normalization."""
    return lhs.normalized() == rhs.normalized()


def match_instantiation_to_facets(
    instantiation: FamilyInstantiation,
    computed_facets: Sequence[LinearInequality],
) -> tuple[FamilyMatch, ...]:
    """Find computed facets exactly reproduced by an instantiated family."""
    matches: list[FamilyMatch] = []
    instantiated = instantiation.inequality.normalized()

    for facet in computed_facets:
        normalized_facet = facet.normalized()
        if instantiated == normalized_facet:
            matches.append(
                FamilyMatch(
                    family_name=instantiation.family_name,
                    parameter=instantiation.parameter,
                    instantiated_inequality=instantiated,
                    computed_facet=normalized_facet,
                    status="exact_match",
                    notes=("Family instantiation normalizes exactly to the computed facet.",),
                )
            )

    return tuple(matches)


def validate_family_instantiation(
    instantiation: FamilyInstantiation,
    *,
    feasible_points: Sequence[Sequence[int | float]],
    computed_facets: Sequence[LinearInequality],
    source: str | None = None,
) -> CandidateFamilyValidation:
    """Validate one instantiated family inequality.

    The validation has two independent gates:

    1. finite validity on enumerated feasible points;
    2. exact matching against computed cdd facets.

    A family instance should not be reported as covering a facet unless
    exact_matches is nonempty.
    """
    finite_validity = check_validity_on_points(
        instantiation.inequality,
        feasible_points,
    )

    exact_matches = match_instantiation_to_facets(instantiation, computed_facets)

    if not finite_validity.is_valid:
        assert finite_validity.violating_point is not None
        assert finite_validity.violation_value is not None
        invalidation = InvalidatedFamilyInstance(
            family_name=instantiation.family_name,
            parameter=instantiation.parameter,
            inequality=instantiation.inequality.normalized(),
            violating_point=finite_validity.violating_point,
            violation_value=finite_validity.violation_value,
            source=source,
            notes=(
                "This candidate family instance is invalid on the enumerated feasible point set.",
            ),
        )
        return CandidateFamilyValidation(
            instantiation=instantiation,
            finite_validity=finite_validity,
            exact_matches=exact_matches,
            invalidation=invalidation,
            status="invalidated",
            notes=("Do not report this family instance as valid or derived.",),
        )

    if exact_matches:
        return CandidateFamilyValidation(
            instantiation=instantiation,
            finite_validity=finite_validity,
            exact_matches=exact_matches,
            invalidation=None,
            status="valid_on_points_and_matches_facets",
            notes=(
                "The family instance is valid on the finite point set and exactly matches at least one computed facet.",
            ),
        )

    return CandidateFamilyValidation(
        instantiation=instantiation,
        finite_validity=finite_validity,
        exact_matches=(),
        invalidation=None,
        status="valid_on_points_but_no_facet_match",
        notes=(
            "The family instance is valid on the finite point set but does not match any computed facet.",
        ),
    )


def validate_family_on_instance(
    family: InequalityFamilyProtocol,
    instance: object,
    *,
    feasible_points: Sequence[Sequence[int | float]],
    computed_facets: Sequence[LinearInequality],
    source: str | None = None,
) -> tuple[CandidateFamilyValidation, ...]:
    """Validate all parameter instantiations of a family on one instance."""
    results: list[CandidateFamilyValidation] = []

    for parameter in family.enumerate_parameters(instance):
        inequality = family.instantiate(instance, parameter)
        instantiation = FamilyInstantiation(
            family_name=family.name,
            parameter=parameter,
            inequality=inequality.normalized(),
        )
        results.append(
            validate_family_instantiation(
                instantiation,
                feasible_points=feasible_points,
                computed_facets=computed_facets,
                source=source,
            )
        )

    return tuple(results)


def summarize_validation_results(
    results: Sequence[CandidateFamilyValidation],
) -> dict[str, int]:
    """Return counts by validation status."""
    summary: dict[str, int] = {}

    for result in results:
        summary[result.status] = summary.get(result.status, 0) + 1

    return summary
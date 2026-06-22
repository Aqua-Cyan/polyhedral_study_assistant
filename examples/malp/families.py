from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence

from psa.family import FamilyParameter, InequalityFamilyProtocol
from psa.inequality import LinearInequality

from .model import MalpInstance


@dataclass(frozen=True)
class FamilyDefinition:
    name: str
    statement: str
    conditions: tuple[str, ...] = ()
    derivation_status: str = "missing"
    family_kind: str = "candidate"


class ActivationRowFamily(InequalityFamilyProtocol):
    def __init__(self, source: str) -> None:
        if source not in {"j1", "j2"}:
            raise ValueError("source must be 'j1' or 'j2'.")
        self.source = source
        self.name = f"activation_{source}"

    def enumerate_parameters(self, instance: object) -> Sequence[FamilyParameter]:
        assert isinstance(instance, MalpInstance)
        return (FamilyParameter({"source": self.source}),)

    def instantiate(self, instance: object, parameter: FamilyParameter) -> LinearInequality:
        assert isinstance(instance, MalpInstance)
        row1, row2 = instance.activation_rows()
        return row1.inequality if self.source == "j1" else row2.inequality


class ResidualFamily(InequalityFamilyProtocol):
    def __init__(self, source: str) -> None:
        if source not in {"j1", "j2"}:
            raise ValueError("source must be 'j1' or 'j2'.")
        self.source = source
        self.name = f"residual_{source}"

    def enumerate_parameters(self, instance: object) -> Sequence[FamilyParameter]:
        assert isinstance(instance, MalpInstance)
        support = tuple(sorted(instance.j1 if self.source == "j1" else instance.j2))
        threshold = instance.b1 if self.source == "j1" else instance.b2

        parameters: list[FamilyParameter] = []
        for subset in nonempty_subsets(support):
            residual = threshold - (len(support) - len(subset))
            if residual <= 0:
                continue
            parameters.append(
                FamilyParameter(
                    {
                        "source": self.source,
                        "subset": subset,
                        "residual": residual,
                    }
                )
            )
        return tuple(parameters)

    def instantiate(self, instance: object, parameter: FamilyParameter) -> LinearInequality:
        assert isinstance(instance, MalpInstance)
        subset = tuple(parameter.values["subset"])
        mapping = instance.variable_map
        coeffs = [0] * instance.dimension
        for element in subset:
            coeffs[mapping.x_index(str(element))] = -1

        if self.source == "j1":
            coeffs[mapping.y1_index] = int(parameter.values["residual"])
        else:
            coeffs[mapping.y2_index] = int(parameter.values["residual"])

        return LinearInequality(tuple(coeffs), 0, "<=").normalized()


class InteractionCandidateFamily(InequalityFamilyProtocol):
    def __init__(self, name: str, statement: str, templates: Sequence[FamilyParameter]) -> None:
        self.name = name
        self.statement = statement
        self.templates = tuple(templates)

    def enumerate_parameters(self, instance: object) -> Sequence[FamilyParameter]:
        _ = instance
        return self.templates

    def instantiate(self, instance: object, parameter: FamilyParameter) -> LinearInequality:
        assert isinstance(instance, MalpInstance)
        mapping = instance.variable_map
        coeffs = [0] * instance.dimension

        for element in parameter.values.get("x_positive", ()):  # type: ignore[union-attr]
            coeffs[mapping.x_index(str(element))] += int(parameter.values.get("x_positive_coeff", 1))
        for element in parameter.values.get("x_negative", ()):  # type: ignore[union-attr]
            coeffs[mapping.x_index(str(element))] -= int(parameter.values.get("x_negative_coeff", 1))

        coeffs[mapping.y1_index] = int(parameter.values.get("y1", 0))
        coeffs[mapping.y2_index] = int(parameter.values.get("y2", 0))
        rhs = int(parameter.values.get("rhs", 0))
        return LinearInequality(tuple(coeffs), rhs, "<=").normalized()


def base_family_definitions() -> tuple[FamilyDefinition, ...]:
    return (
        FamilyDefinition(
            name="Residual family for J1",
            statement="x(D) >= (b_1 - |J_1 \\ D|) y_1",
            conditions=("D subset J_1", "b_1 - |J_1 \\ D| > 0"),
            derivation_status="passed",
            family_kind="derived",
        ),
        FamilyDefinition(
            name="Residual family for J2",
            statement="x(D) >= (b_2 - |J_2 \\ D|) y_2",
            conditions=("D subset J_2", "b_2 - |J_2 \\ D| > 0"),
            derivation_status="passed",
            family_kind="derived",
        ),
    )


def seed_families() -> tuple[InequalityFamilyProtocol, ...]:
    return (
        ActivationRowFamily("j1"),
        ActivationRowFamily("j2"),
        ResidualFamily("j1"),
        ResidualFamily("j2"),
    )


def nonempty_subsets(elements: Iterable[str]) -> tuple[tuple[str, ...], ...]:
    ordered = tuple(sorted(elements))
    subsets: list[tuple[str, ...]] = []
    for size in range(1, len(ordered) + 1):
        subsets.extend(combinations(ordered, size))
    return tuple(subsets)


def family_group_key(statement: str, y_coefficients: tuple[int, int]) -> tuple[str, tuple[int, int]]:
    return statement, y_coefficients

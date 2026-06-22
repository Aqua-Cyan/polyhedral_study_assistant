from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence

from psa.binary_points import BinaryPoint, enumerate_binary_points
from psa.cmir import SourceRow, convert_activation_lower_row
from psa.family import normalized_equal
from psa.inequality import LinearInequality
from psa.report import format_inequality


@dataclass(frozen=True)
class MalpVariableMap:
    ground: tuple[str, ...]

    @property
    def x_indices(self) -> tuple[int, ...]:
        return tuple(range(len(self.ground)))

    @property
    def y1_index(self) -> int:
        return len(self.ground)

    @property
    def y2_index(self) -> int:
        return len(self.ground) + 1

    @property
    def variable_names(self) -> tuple[str, ...]:
        x_names = tuple(f"x_{name}" for name in self.ground)
        return x_names + ("y_1", "y_2")

    def x_index(self, element: str) -> int:
        return self.ground.index(element)


@dataclass(frozen=True)
class MalpInstance:
    name: str
    j1: frozenset[str]
    j2: frozenset[str]
    b1: int
    b2: int

    def __post_init__(self) -> None:
        if not self.j1:
            raise ValueError("J1 must be nonempty.")
        if not self.j2:
            raise ValueError("J2 must be nonempty.")
        if not (1 <= self.b1 <= len(self.j1)):
            raise ValueError("b1 must satisfy 1 <= b1 <= |J1|.")
        if not (1 <= self.b2 <= len(self.j2)):
            raise ValueError("b2 must satisfy 1 <= b2 <= |J2|.")

    @property
    def ground(self) -> tuple[str, ...]:
        return tuple(sorted(self.j1 | self.j2))

    @property
    def variable_map(self) -> MalpVariableMap:
        return MalpVariableMap(self.ground)

    @property
    def dimension(self) -> int:
        return len(self.ground) + 2

    @property
    def j1_only(self) -> frozenset[str]:
        return self.j1 - self.j2

    @property
    def j12(self) -> frozenset[str]:
        return self.j1 & self.j2

    @property
    def j2_only(self) -> frozenset[str]:
        return self.j2 - self.j1

    @property
    def region_signature(self) -> tuple[int, int, int]:
        return (len(self.j1_only), len(self.j12), len(self.j2_only))

    def x_sum(self, point: Sequence[int], elements: Iterable[str]) -> int:
        mapping = self.variable_map
        return sum(point[mapping.x_index(element)] for element in elements)

    def is_feasible_point(self, point: Sequence[int]) -> bool:
        if len(point) != self.dimension:
            raise ValueError("Point dimension does not match instance dimension.")
        if any(value not in (0, 1) for value in point):
            return False

        mapping = self.variable_map
        y1 = point[mapping.y1_index]
        y2 = point[mapping.y2_index]
        return self.x_sum(point, self.j1) >= self.b1 * y1 and self.x_sum(point, self.j2) >= self.b2 * y2

    def enumerate_feasible_points(self) -> list[BinaryPoint]:
        return enumerate_binary_points(self.dimension, predicate=self.is_feasible_point)

    def activation_rows(self) -> tuple[SourceRow, SourceRow]:
        mapping = self.variable_map
        coeffs1 = [0] * self.dimension
        coeffs2 = [0] * self.dimension

        for element in self.j1:
            coeffs1[mapping.x_index(element)] = -1
        coeffs1[mapping.y1_index] = self.b1

        for element in self.j2:
            coeffs2[mapping.x_index(element)] = -1
        coeffs2[mapping.y2_index] = self.b2

        row1 = convert_activation_lower_row(
            name=f"{self.name}:activation_j1",
            inequality=LinearInequality(tuple(coeffs1), 0, "<="),
            symbolic_form=f"x(J_1) >= {self.b1} y_1",
            x_support=tuple(sorted(mapping.x_index(element) for element in self.j1)),
            y_index=mapping.y1_index,
            threshold=self.b1,
            notes=(f"J1={sorted(self.j1)!r}",),
        )
        row2 = convert_activation_lower_row(
            name=f"{self.name}:activation_j2",
            inequality=LinearInequality(tuple(coeffs2), 0, "<="),
            symbolic_form=f"x(J_2) >= {self.b2} y_2",
            x_support=tuple(sorted(mapping.x_index(element) for element in self.j2)),
            y_index=mapping.y2_index,
            threshold=self.b2,
            notes=(f"J2={sorted(self.j2)!r}",),
        )
        return row1, row2

    def inequality_to_string(self, inequality: LinearInequality) -> str:
        return format_inequality(inequality.normalized(), self.variable_map.variable_names)


@dataclass(frozen=True)
class MalpFacetRecord:
    instance_name: str
    inequality: LinearInequality
    classification: str
    rendered: str
    x_support_names: tuple[str, ...]
    y_coefficients: tuple[int, int]
    support_signature: str


@dataclass(frozen=True)
class ClassifiedFacets:
    bounds: tuple[MalpFacetRecord, ...]
    original_constraints: tuple[MalpFacetRecord, ...]
    nontrivial: tuple[MalpFacetRecord, ...]


@dataclass(frozen=True)
class InstanceRun:
    stage: str
    instance: MalpInstance


@dataclass(frozen=True)
class EquationHandlingNote:
    message: str = (
        "The current cdd backend skips equations returned by pycddlib; if equations occur, "
        "the report must state this backend limitation explicitly."
    )


def powerset(elements: Iterable[str]) -> tuple[tuple[str, ...], ...]:
    ordered = tuple(sorted(elements))
    subsets: list[tuple[str, ...]] = []
    for size in range(len(ordered) + 1):
        subsets.extend(combinations(ordered, size))
    return tuple(subsets)


def make_variable_bound_inequalities(instance: MalpInstance) -> tuple[LinearInequality, ...]:
    mapping = instance.variable_map
    inequalities: list[LinearInequality] = []
    for index in range(instance.dimension):
        upper_coeffs = [0] * instance.dimension
        upper_coeffs[index] = 1
        inequalities.append(LinearInequality(tuple(upper_coeffs), 1, "<=").normalized())
        lower_coeffs = [0] * instance.dimension
        lower_coeffs[index] = -1
        inequalities.append(LinearInequality(tuple(lower_coeffs), 0, "<=").normalized())
    return tuple(inequalities)


def classify_facets(
    instance: MalpInstance,
    inequalities: Sequence[LinearInequality],
) -> ClassifiedFacets:
    bounds: list[MalpFacetRecord] = []
    original_constraints: list[MalpFacetRecord] = []
    nontrivial: list[MalpFacetRecord] = []

    bound_set = set(make_variable_bound_inequalities(instance))
    source_rows = instance.activation_rows()
    source_set = {row.inequality.normalized() for row in source_rows}

    mapping = instance.variable_map
    for inequality in inequalities:
        normalized = inequality.normalized()
        classification = "nontrivial"
        if normalized in bound_set:
            classification = "variable_bound"
        elif normalized in source_set:
            classification = "original_constraint"

        x_support_names = tuple(
            mapping.ground[index]
            for index in normalized.support
            if index < len(mapping.ground)
        )
        y_coefficients = (
            normalized.coefficients[mapping.y1_index],
            normalized.coefficients[mapping.y2_index],
        )
        signature = _facet_signature(instance, normalized)
        record = MalpFacetRecord(
            instance_name=instance.name,
            inequality=normalized,
            classification=classification,
            rendered=instance.inequality_to_string(normalized),
            x_support_names=x_support_names,
            y_coefficients=y_coefficients,
            support_signature=signature,
        )
        if classification == "variable_bound":
            bounds.append(record)
        elif classification == "original_constraint":
            original_constraints.append(record)
        else:
            nontrivial.append(record)

    return ClassifiedFacets(tuple(bounds), tuple(original_constraints), tuple(nontrivial))


def _facet_signature(instance: MalpInstance, inequality: LinearInequality) -> str:
    mapping = instance.variable_map
    names = {
        mapping.ground[index]
        for index in inequality.support
        if index < len(mapping.ground)
    }
    j1_only = len(names & instance.j1_only)
    j12 = len(names & instance.j12)
    j2_only = len(names & instance.j2_only)
    y1 = inequality.coefficients[mapping.y1_index]
    y2 = inequality.coefficients[mapping.y2_index]
    return f"x[{j1_only},{j12},{j2_only}]|y[{y1},{y2}]|rhs={inequality.rhs}"


def make_instance(
    name: str,
    j1: Iterable[str],
    j2: Iterable[str],
    b1: int,
    b2: int,
) -> MalpInstance:
    return MalpInstance(name=name, j1=frozenset(j1), j2=frozenset(j2), b1=b1, b2=b2)


def generate_staged_instances() -> tuple[InstanceRun, ...]:
    runs: list[InstanceRun] = []

    def add(stage: str, instance: MalpInstance) -> None:
        runs.append(InstanceRun(stage=stage, instance=instance))

    add("sanity", make_instance("sanity_disjoint_2", ["a", "b"], ["c", "d"], 1, 1))
    add("sanity", make_instance("sanity_overlap_1", ["a", "b"], ["b", "c"], 1, 1))

    add("structured", make_instance("disjoint_3x3", ["a", "b", "c"], ["d", "e", "f"], 2, 2))
    add("structured", make_instance("overlap_1", ["a", "b", "c"], ["c", "d", "e"], 2, 2))
    add("structured", make_instance("overlap_2", ["a", "b", "c", "d"], ["c", "d", "e"], 2, 2))
    add("structured", make_instance("nested_j1_in_j2", ["a", "b"], ["a", "b", "c", "d"], 1, 3))
    add("structured", make_instance("nested_j2_in_j1", ["a", "b", "c", "d"], ["b", "c"], 3, 1))
    add("structured", make_instance("identical", ["a", "b", "c"], ["a", "b", "c"], 1, 2))
    add("structured", make_instance("boundary_full", ["a", "b", "c"], ["b", "c", "d"], 3, 1))

    add("medium", make_instance("medium_overlap_5", ["a", "b", "c", "d"], ["c", "d", "e", "f"], 2, 3))
    add("medium", make_instance("medium_identical_5", ["a", "b", "c", "d", "e"], ["a", "b", "c", "d", "e"], 2, 4))
    add("medium", make_instance("medium_nested_6", ["a", "b", "c"], ["a", "b", "c", "d", "e", "f"], 2, 4))

    add("sweep", make_instance("sweep_421", ["a", "b", "c", "d"], ["c", "d", "e"], 1, 2))
    add("sweep", make_instance("sweep_422", ["a", "b", "c", "d"], ["b", "c", "d", "e"], 2, 2))
    add("sweep", make_instance("sweep_431", ["a", "b", "c", "d"], ["a", "d", "e", "f"], 3, 1))

    return tuple(runs)


def find_matching_facet(
    target: LinearInequality,
    facets: Sequence[MalpFacetRecord],
) -> MalpFacetRecord | None:
    for facet in facets:
        if normalized_equal(target, facet.inequality):
            return facet
    return None

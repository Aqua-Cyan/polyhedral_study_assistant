from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable, Sequence

from psa.backends.cdd import convex_hull_inequalities_from_points
from psa.inequality import LinearInequality


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROBLEM_ID = "malp"

REPORTS_DIR = PROJECT_ROOT / "reports"
TASKS_DIR = PROJECT_ROOT / "tasks"
MEMORY_DIR = PROJECT_ROOT / "memory"

STATE_PATH = REPORTS_DIR / "malp_state.json"
REPORT_PATH = REPORTS_DIR / "malp_report.md"
TASK_POOL_PATH = TASKS_DIR / "TASK_POOL.json"

FACET_MEMORY_DIR = MEMORY_DIR / "facets" / PROBLEM_ID
FAMILY_MEMORY_DIR = MEMORY_DIR / "family" / PROBLEM_ID

FACET_SIGNATURES_PATH = FACET_MEMORY_DIR / "facet_signatures.json"
FAMILY_MEMORY_PATH = FAMILY_MEMORY_DIR / "family_memory.json"


@dataclass(frozen=True)
class MalpInstance:
    """Canonical finite MALP instance.

    Internally we use the partition

        O = J1 \\ J2
        I = J1 ∩ J2
        K = J2 \\ J1

    with variable order:

        o1, ..., o_p, i1, ..., i_q, k1, ..., k_r, y1, y2

    This is an internal computational representation. Reports should still
    translate statements back to the user's original notation J1, J2.
    """

    o_size: int
    i_size: int
    k_size: int
    b1: int
    b2: int

    @property
    def union_size(self) -> int:
        return self.o_size + self.i_size + self.k_size

    @property
    def j1_size(self) -> int:
        return self.o_size + self.i_size

    @property
    def j2_size(self) -> int:
        return self.i_size + self.k_size

    @property
    def dimension(self) -> int:
        return self.union_size + 2

    @property
    def y1_index(self) -> int:
        return self.union_size

    @property
    def y2_index(self) -> int:
        return self.union_size + 1

    @property
    def o_indices(self) -> tuple[int, ...]:
        return tuple(range(self.o_size))

    @property
    def i_indices(self) -> tuple[int, ...]:
        start = self.o_size
        return tuple(range(start, start + self.i_size))

    @property
    def k_indices(self) -> tuple[int, ...]:
        start = self.o_size + self.i_size
        return tuple(range(start, start + self.k_size))

    @property
    def j1_indices(self) -> tuple[int, ...]:
        return self.o_indices + self.i_indices

    @property
    def j2_indices(self) -> tuple[int, ...]:
        return self.i_indices + self.k_indices

    @property
    def variable_names(self) -> tuple[str, ...]:
        names: list[str] = []
        names.extend(f"o{idx + 1}" for idx in range(self.o_size))
        names.extend(f"i{idx + 1}" for idx in range(self.i_size))
        names.extend(f"k{idx + 1}" for idx in range(self.k_size))
        names.extend(("y1", "y2"))
        return tuple(names)

    @property
    def relation(self) -> str:
        if self.i_size == 0:
            return "disjoint"
        if self.o_size == 0 and self.k_size == 0:
            return "identical"
        if self.o_size == 0 or self.k_size == 0:
            return "nested"
        return "overlap"

    @property
    def label(self) -> str:
        return (
            f"O={self.o_size},I={self.i_size},K={self.k_size},"
            f"b1={self.b1},b2={self.b2}"
        )

    def is_admissible(self) -> bool:
        return (
            self.union_size > 0
            and self.j1_size > 0
            and self.j2_size > 0
            and 1 <= self.b1 <= self.j1_size
            and 1 <= self.b2 <= self.j2_size
        )

    def feasible(self, point: tuple[int, ...]) -> bool:
        if len(point) != self.dimension:
            return False

        lhs_j1 = sum(point[index] for index in self.j1_indices)
        lhs_j2 = sum(point[index] for index in self.j2_indices)
        y1 = point[self.y1_index]
        y2 = point[self.y2_index]

        return lhs_j1 >= self.b1 * y1 and lhs_j2 >= self.b2 * y2

    def enumerate_feasible_points(self) -> tuple[tuple[int, ...], ...]:
        points = []
        for point in product((0, 1), repeat=self.dimension):
            if self.feasible(point):
                points.append(tuple(point))
        return tuple(points)

    def base_activation_inequalities(self) -> tuple[LinearInequality, LinearInequality]:
        coeffs_1 = [0] * self.dimension
        for index in self.j1_indices:
            coeffs_1[index] = -1
        coeffs_1[self.y1_index] = self.b1

        coeffs_2 = [0] * self.dimension
        for index in self.j2_indices:
            coeffs_2[index] = -1
        coeffs_2[self.y2_index] = self.b2

        return (
            LinearInequality(tuple(coeffs_1), 0, "<=").normalized(),
            LinearInequality(tuple(coeffs_2), 0, "<=").normalized(),
        )

    def trivial_bounds(self) -> tuple[LinearInequality, ...]:
        inequalities: list[LinearInequality] = []

        for index in range(self.dimension):
            upper = [0] * self.dimension
            upper[index] = 1
            inequalities.append(LinearInequality(tuple(upper), 1, "<=").normalized())

            lower = [0] * self.dimension
            lower[index] = -1
            inequalities.append(LinearInequality(tuple(lower), 0, "<=").normalized())

        return tuple(inequalities)

    def as_state_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "o_size": self.o_size,
            "i_size": self.i_size,
            "k_size": self.k_size,
            "b1": self.b1,
            "b2": self.b2,
            "relation": self.relation,
            "union_size": self.union_size,
            "j1_size": self.j1_size,
            "j2_size": self.j2_size,
            "dimension": self.dimension,
            "variable_names": list(self.variable_names),
            "o_indices": list(self.o_indices),
            "i_indices": list(self.i_indices),
            "k_indices": list(self.k_indices),
            "j1_indices": list(self.j1_indices),
            "j2_indices": list(self.j2_indices),
            "y1_index": self.y1_index,
            "y2_index": self.y2_index,
        }


@dataclass(frozen=True)
class FacetRecord:
    inequality: LinearInequality
    kind: str
    text: str
    signature: str
    family_status: str
    matched_family: str | None
    derivation_status: str
    instance_label: str


@dataclass(frozen=True)
class InstanceAnalysis:
    instance: MalpInstance
    feasible_point_count: int
    facet_count: int
    records: tuple[FacetRecord, ...]


def ensure_dirs() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    FACET_MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    FAMILY_MEMORY_DIR.mkdir(parents=True, exist_ok=True)


def inequality_to_dict(inequality: LinearInequality) -> dict[str, Any]:
    normalized = inequality.normalized()
    return {
        "coefficients": list(normalized.coefficients),
        "rhs": normalized.rhs,
        "sense": normalized.sense,
        "support": list(normalized.support),
    }


def format_inequality(inequality: LinearInequality, variable_names: Sequence[str]) -> str:
    normalized = inequality.normalized()
    terms: list[str] = []

    for coefficient, name in zip(normalized.coefficients, variable_names, strict=True):
        if coefficient == 0:
            continue

        magnitude = abs(coefficient)
        atom = name if magnitude == 1 else f"{magnitude} {name}"

        if not terms:
            terms.append(atom if coefficient > 0 else f"-{atom}")
        else:
            sign = "+" if coefficient > 0 else "-"
            terms.append(f"{sign} {atom}")

    lhs = " ".join(terms) if terms else "0"
    return f"{lhs} {normalized.sense} {normalized.rhs}"


def subset_name(instance: MalpInstance, indices: Iterable[int]) -> str:
    names = instance.variable_names
    return "{" + ", ".join(names[index] for index in sorted(indices)) + "}"


def classify_signature(instance: MalpInstance, inequality: LinearInequality) -> str:
    coeffs = inequality.normalized().coefficients

    x_indices = tuple(index for index in range(instance.union_size) if coeffs[index] != 0)
    x_coeffs = tuple(coeffs[index] for index in x_indices)

    y1_coeff = coeffs[instance.y1_index]
    y2_coeff = coeffs[instance.y2_index]

    support_regions = {
        "O": sum(1 for idx in x_indices if idx in instance.o_indices),
        "I": sum(1 for idx in x_indices if idx in instance.i_indices),
        "K": sum(1 for idx in x_indices if idx in instance.k_indices),
    }

    x_unit_negative = all(coefficient == -1 for coefficient in x_coeffs)

    if y1_coeff == 0 and y2_coeff == 0:
        y_pattern = "no_y"
    elif y1_coeff != 0 and y2_coeff == 0:
        y_pattern = f"y1={y1_coeff}"
    elif y1_coeff == 0 and y2_coeff != 0:
        y_pattern = f"y2={y2_coeff}"
    else:
        y_pattern = f"y1={y1_coeff},y2={y2_coeff}"

    return (
        f"relation={instance.relation};"
        f"O={support_regions['O']},I={support_regions['I']},K={support_regions['K']};"
        f"x_unit_negative={x_unit_negative};"
        f"{y_pattern};rhs={inequality.normalized().rhs}"
    )


def residual_match(instance: MalpInstance, inequality: LinearInequality) -> tuple[bool, str | None]:
    """Recognize one-row residual family exactly.

    This is intentionally conservative. More complex interaction families are not
    promoted here.
    """
    normalized = inequality.normalized()
    coeffs = normalized.coefficients

    nonzero_y = [
        index
        for index in (instance.y1_index, instance.y2_index)
        if coeffs[index] != 0
    ]

    if len(nonzero_y) != 1:
        return False, None

    y_index = nonzero_y[0]
    source_indices = instance.j1_indices if y_index == instance.y1_index else instance.j2_indices
    threshold = instance.b1 if y_index == instance.y1_index else instance.b2
    family_name = "single_activation_residual_j1" if y_index == instance.y1_index else "single_activation_residual_j2"

    x_support = tuple(
        index
        for index in range(instance.union_size)
        if coeffs[index] != 0
    )

    if not set(x_support).issubset(set(source_indices)):
        return False, None

    if any(coeffs[index] != -1 for index in x_support):
        return False, None

    residual = threshold - (len(source_indices) - len(x_support))

    if residual <= 0:
        return False, None

    expected_coeffs = [0] * instance.dimension
    for index in x_support:
        expected_coeffs[index] = -1
    expected_coeffs[y_index] = residual

    expected = LinearInequality(tuple(expected_coeffs), 0, "<=").normalized()

    if expected == normalized:
        return True, family_name

    return False, None


def classify_facet(instance: MalpInstance, inequality: LinearInequality) -> tuple[str, str, str | None, str]:
    normalized = inequality.normalized()

    if normalized in set(instance.trivial_bounds()):
        return "bound", "derived", "variable_bounds", "proved_from_binary_domain"

    base_1, base_2 = instance.base_activation_inequalities()
    if normalized == base_1:
        return "original_constraint", "derived", "activation_j1", "model_definition"
    if normalized == base_2:
        return "original_constraint", "derived", "activation_j2", "model_definition"

    is_residual, residual_family = residual_match(instance, normalized)
    if is_residual:
        return "nontrivial", "derived", residual_family, "residual_certificate_available"

    coeffs = normalized.coefficients
    has_y1 = coeffs[instance.y1_index] != 0
    has_y2 = coeffs[instance.y2_index] != 0

    if has_y1 and has_y2:
        return "nontrivial", "candidate", None, "interaction_derivation_missing"

    return "nontrivial", "unresolved", None, "no_family_match_yet"


def analyze_instance(instance: MalpInstance) -> InstanceAnalysis:
    feasible_points = instance.enumerate_feasible_points()
    hull_inequalities = convex_hull_inequalities_from_points(feasible_points)

    records: list[FacetRecord] = []
    for inequality in hull_inequalities:
        normalized = inequality.normalized()
        kind, family_status, matched_family, derivation_status = classify_facet(instance, normalized)
        text = format_inequality(normalized, instance.variable_names)
        signature = classify_signature(instance, normalized)

        records.append(
            FacetRecord(
                inequality=normalized,
                kind=kind,
                text=text,
                signature=signature,
                family_status=family_status,
                matched_family=matched_family,
                derivation_status=derivation_status,
                instance_label=instance.label,
            )
        )

    return InstanceAnalysis(
        instance=instance,
        feasible_point_count=len(feasible_points),
        facet_count=len(records),
        records=tuple(records),
    )


def generate_instances(max_union_size: int) -> tuple[MalpInstance, ...]:
    """Generate a staged MALP sweep.

    The sweep is deliberately modest because pycddlib hull extraction can grow
    quickly. The purpose is to create enough pressure to discourage overfitting
    to tiny examples.
    """
    instances: list[MalpInstance] = []

    for o_size in range(0, max_union_size + 1):
        for i_size in range(0, max_union_size + 1):
            for k_size in range(0, max_union_size + 1):
                union_size = o_size + i_size + k_size
                if union_size == 0 or union_size > max_union_size:
                    continue

                j1_size = o_size + i_size
                j2_size = i_size + k_size

                if j1_size == 0 or j2_size == 0:
                    continue

                for b1 in range(1, j1_size + 1):
                    for b2 in range(1, j2_size + 1):
                        instance = MalpInstance(
                            o_size=o_size,
                            i_size=i_size,
                            k_size=k_size,
                            b1=b1,
                            b2=b2,
                        )
                        if instance.is_admissible():
                            instances.append(instance)

    return tuple(instances)


def facet_record_to_state(record: FacetRecord, instance: MalpInstance) -> dict[str, Any]:
    return {
        "instance": instance.as_state_dict(),
        "kind": record.kind,
        "text": record.text,
        "signature": record.signature,
        "family_status": record.family_status,
        "matched_family": record.matched_family,
        "derivation_status": record.derivation_status,
        "inequality": inequality_to_dict(record.inequality),
    }


def build_state(analyses: Sequence[InstanceAnalysis], max_union_size: int) -> dict[str, Any]:
    all_records: list[tuple[InstanceAnalysis, FacetRecord]] = []
    for analysis in analyses:
        for record in analysis.records:
            all_records.append((analysis, record))

    derived = [
        facet_record_to_state(record, analysis.instance)
        for analysis, record in all_records
        if record.family_status == "derived"
    ]
    candidates = [
        facet_record_to_state(record, analysis.instance)
        for analysis, record in all_records
        if record.family_status == "candidate"
    ]
    unresolved = [
        facet_record_to_state(record, analysis.instance)
        for analysis, record in all_records
        if record.family_status == "unresolved"
    ]

    signature_groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for analysis, record in all_records:
        if record.kind == "nontrivial":
            signature_groups[record.signature].append(
                {
                    "instance_label": analysis.instance.label,
                    "text": record.text,
                    "family_status": record.family_status,
                    "matched_family": record.matched_family,
                    "derivation_status": record.derivation_status,
                    "inequality": inequality_to_dict(record.inequality),
                }
            )

    family_counts: dict[str, int] = defaultdict(int)
    for _, record in all_records:
        if record.matched_family is not None:
            family_counts[record.matched_family] += 1

    stop_status = "done" if not candidates and not unresolved else "continue"

    proof_obligations = []
    if candidates:
        proof_obligations.append(
            "Candidate interaction facets remain. Run FamilyGuesser and DerivationProver on interaction signatures."
        )
    if unresolved:
        proof_obligations.append(
            "Unresolved facets remain. Perform source identification, MIR-over-MIR attempts, and family compression."
        )
    if not candidates and not unresolved:
        proof_obligations.append(
            "All currently computed facets are classified by derived families in this tested scope. A full convex-hull theorem still requires validity and reverse-inclusion proof."
        )

    return {
        "problem_id": PROBLEM_ID,
        "problem_name": "MALP",
        "state_version": 1,
        "tested_scope": {
            "max_union_size": max_union_size,
            "instance_count": len(analyses),
            "backend": "pycddlib through psa.backends.cdd.convex_hull_inequalities_from_points",
        },
        "summary": {
            "instances": len(analyses),
            "facets_total": sum(analysis.facet_count for analysis in analyses),
            "derived_records": len(derived),
            "candidate_records": len(candidates),
            "unresolved_records": len(unresolved),
            "signature_count": len(signature_groups),
            "stop_status": stop_status,
        },
        "instances": [
            {
                "instance": analysis.instance.as_state_dict(),
                "feasible_point_count": analysis.feasible_point_count,
                "facet_count": analysis.facet_count,
            }
            for analysis in analyses
        ],
        "derived_families": [
            {
                "name": "variable_bounds",
                "status": "derived",
                "reason": "binary domain",
                "covered_records": family_counts.get("variable_bounds", 0),
            },
            {
                "name": "activation_j1",
                "status": "derived",
                "reason": "original model constraint",
                "covered_records": family_counts.get("activation_j1", 0),
            },
            {
                "name": "activation_j2",
                "status": "derived",
                "reason": "original model constraint",
                "covered_records": family_counts.get("activation_j2", 0),
            },
            {
                "name": "single_activation_residual_j1",
                "status": "derived",
                "reason": "residual from x(J1) >= b1 y1",
                "covered_records": family_counts.get("single_activation_residual_j1", 0),
            },
            {
                "name": "single_activation_residual_j2",
                "status": "derived",
                "reason": "residual from x(J2) >= b2 y2",
                "covered_records": family_counts.get("single_activation_residual_j2", 0),
            },
        ],
        "candidate_facets": candidates,
        "unresolved_facets": unresolved,
        "facet_signature_groups": [
            {
                "signature": signature,
                "count": len(items),
                "examples": items[:20],
                "truncated": len(items) > 20,
            }
            for signature, items in sorted(signature_groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        ],
        "proof_obligations": proof_obligations,
    }


def build_task_pool_entries(state: dict[str, Any]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []

    for index, group in enumerate(state["facet_signature_groups"], start=1):
        examples = group["examples"]
        has_candidate = any(example["family_status"] == "candidate" for example in examples)
        has_unresolved = any(example["family_status"] == "unresolved" for example in examples)

        if not has_candidate and not has_unresolved:
            continue

        task_type = "derive_interaction_family" if has_candidate else "analyze_unresolved_signature"

        tasks.append(
            {
                "id": f"{PROBLEM_ID}-{task_type}-{index:04d}",
                "problem_id": PROBLEM_ID,
                "type": task_type,
                "status": "open",
                "priority": 1 if has_candidate else 2,
                "signature": group["signature"],
                "facet_count": group["count"],
                "sample_facets": examples[:5],
                "assigned_agent": "DerivationProver",
                "required_actions": [
                    "identify source constraints",
                    "try residual",
                    "try coefficient tightening",
                    "try aggregation+c-MIR",
                    "try mixed MIR",
                    "try MIR-over-MIR / derived-row reuse",
                    "propose general family if repeated pattern is found",
                    "run exact matching and finite validity gates",
                ],
                "success_criterion": (
                    "Produce a derived family with certificate, or produce a more specific blocker "
                    "explaining why this signature remains unresolved."
                ),
            }
        )

    if len(state["candidate_facets"]) >= 5:
        tasks.append(
            {
                "id": f"{PROBLEM_ID}-family-compression-0001",
                "problem_id": PROBLEM_ID,
                "type": "family_compression",
                "status": "open",
                "priority": 1,
                "assigned_agent": "FamilyGuesser",
                "candidate_count": len(state["candidate_facets"]),
                "required_actions": [
                    "cluster candidate facets by support and coefficient pattern",
                    "search for a common parameterized family",
                    "express family using D, J1\\D, J2\\D, intersections, and threshold residuals",
                    "instantiate proposed family on all tested instances",
                    "send to Verifier for exact matching and finite validity",
                ],
                "success_criterion": (
                    "Replace multiple local candidate families with a smaller number of general "
                    "parameterized candidate families, or explain why compression failed."
                ),
            }
        )

    return tasks


def merge_task_pool(new_tasks: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    if TASK_POOL_PATH.exists():
        try:
            existing = json.loads(TASK_POOL_PATH.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except json.JSONDecodeError:
            existing = []
    else:
        existing = []

    by_id: dict[str, dict[str, Any]] = {}

    for task in existing:
        task_id = task.get("id")
        if isinstance(task_id, str):
            by_id[task_id] = task

    for task in new_tasks:
        task_id = task["id"]
        old = by_id.get(task_id)
        if old is not None and old.get("status") in {"done", "closed"}:
            continue
        by_id[task_id] = task

    return list(by_id.values())


def write_json(path: Path, data: Any) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False),
        encoding="utf-8",
    )


def write_state_outputs(state: dict[str, Any]) -> None:
    write_json(STATE_PATH, state)

    facet_memory = {
        "problem_id": PROBLEM_ID,
        "signature_groups": state["facet_signature_groups"],
        "summary": state["summary"],
    }
    write_json(FACET_SIGNATURES_PATH, facet_memory)

    family_memory = {
        "problem_id": PROBLEM_ID,
        "derived_families": state["derived_families"],
        "candidate_family_count": len(state["candidate_facets"]),
        "unresolved_facet_count": len(state["unresolved_facets"]),
        "notes": [
            "This file is problem-specific memory for MALP.",
            "Do not mix it with other problems. Use memory/family/<problem_id>/ for each new study.",
        ],
    }
    write_json(FAMILY_MEMORY_PATH, family_memory)

    new_tasks = build_task_pool_entries(state)
    merged_tasks = merge_task_pool(new_tasks)
    write_json(TASK_POOL_PATH, merged_tasks)


def render_report(state: dict[str, Any]) -> str:
    lines: list[str] = []

    summary = state["summary"]
    scope = state["tested_scope"]

    lines.extend(
        [
            "# MALP research state report",
            "",
            "## Scope",
            "",
            f"- problem_id: `{state['problem_id']}`",
            f"- max tested union size: `{scope['max_union_size']}`",
            f"- tested instances: `{summary['instances']}`",
            f"- total computed facets/inequalities: `{summary['facets_total']}`",
            f"- derived records: `{summary['derived_records']}`",
            f"- candidate records: `{summary['candidate_records']}`",
            f"- unresolved records: `{summary['unresolved_records']}`",
            f"- stop status: `{summary['stop_status']}`",
            "",
            "Computed facets are evidence. This report is not a complete convex-hull proof.",
            "",
            "## Derived families currently recognized",
            "",
            "| family | status | covered records | reason |",
            "| --- | --- | ---: | --- |",
        ]
    )

    for family in state["derived_families"]:
        lines.append(
            f"| `{family['name']}` | `{family['status']}` | {family['covered_records']} | {family['reason']} |"
        )

    lines.extend(
        [
            "",
            "## Candidate and unresolved status",
            "",
            f"- candidate facets: `{len(state['candidate_facets'])}`",
            f"- unresolved facets: `{len(state['unresolved_facets'])}`",
            "",
        ]
    )

    if state["candidate_facets"]:
        lines.extend(["### Candidate facet examples", ""])
        for item in state["candidate_facets"][:20]:
            lines.append(
                f"- `{item['text']}` from `{item['instance']['label']}`; "
                f"signature: `{item['signature']}`"
            )
        if len(state["candidate_facets"]) > 20:
            lines.append(f"- ... truncated {len(state['candidate_facets']) - 20} more candidate facets")
        lines.append("")

    if state["unresolved_facets"]:
        lines.extend(["### Unresolved facet examples", ""])
        for item in state["unresolved_facets"][:20]:
            lines.append(
                f"- `{item['text']}` from `{item['instance']['label']}`; "
                f"signature: `{item['signature']}`"
            )
        if len(state["unresolved_facets"]) > 20:
            lines.append(f"- ... truncated {len(state['unresolved_facets']) - 20} more unresolved facets")
        lines.append("")

    lines.extend(
        [
            "## Facet signature groups",
            "",
            "| count | signature | recommended action |",
            "| ---: | --- | --- |",
        ]
    )

    for group in state["facet_signature_groups"][:30]:
        examples = group["examples"]
        statuses = {example["family_status"] for example in examples}
        if "candidate" in statuses:
            action = "derive or compress interaction family"
        elif "unresolved" in statuses:
            action = "run source identification and MIR-over-MIR attempts"
        else:
            action = "covered"
        lines.append(f"| {group['count']} | `{group['signature']}` | {action} |")

    lines.extend(["", "## Proof obligations", ""])
    for obligation in state["proof_obligations"]:
        lines.append(f"- {obligation}")

    lines.extend(
        [
            "",
            "## Generated machine-readable artifacts",
            "",
            f"- `{STATE_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{TASK_POOL_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{FACET_SIGNATURES_PATH.relative_to(PROJECT_ROOT)}`",
            f"- `{FAMILY_MEMORY_PATH.relative_to(PROJECT_ROOT)}`",
            "",
        ]
    )

    return "\n".join(lines)


def run(max_union_size: int) -> dict[str, Any]:
    ensure_dirs()

    instances = generate_instances(max_union_size=max_union_size)
    analyses: list[InstanceAnalysis] = []

    for counter, instance in enumerate(instances, start=1):
        print(f"[{counter}/{len(instances)}] analyzing {instance.label}")
        analyses.append(analyze_instance(instance))

    state = build_state(analyses, max_union_size=max_union_size)
    write_state_outputs(state)

    report = render_report(state)
    REPORT_PATH.write_text(report, encoding="utf-8")

    return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MALP convex-hull research state generation.")
    parser.add_argument(
        "--max-union-size",
        type=int,
        default=5,
        help="Maximum |J1 union J2| to enumerate. Increase cautiously.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    state = run(max_union_size=args.max_union_size)

    print("")
    print("MALP study complete.")
    print(f"state: {STATE_PATH}")
    print(f"report: {REPORT_PATH}")
    print(f"task pool: {TASK_POOL_PATH}")
    print(f"facet memory: {FACET_SIGNATURES_PATH}")
    print(f"family memory: {FAMILY_MEMORY_PATH}")
    print(f"stop_status: {state['summary']['stop_status']}")


if __name__ == "__main__":
    main()

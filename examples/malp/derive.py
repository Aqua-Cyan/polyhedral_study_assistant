from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Sequence

from psa.cmir import CmirAttempt, CmirAttemptor, CmirRequest, SourceRow
from psa.family import FamilyParameter, normalized_equal
from psa.inequality import LinearInequality
from psa.report import DerivationAttempt, DerivationStep, SourceConstraint

from .families import InteractionCandidateFamily
from .model import MalpFacetRecord, MalpInstance, find_matching_facet


@dataclass(frozen=True)
class MalpDerivedRow:
    name: str
    inequality: LinearInequality
    symbolic_form: str
    stage: str
    source_rows: tuple[SourceRow, ...]

    def as_source_row(self) -> SourceRow:
        return SourceRow(
            name=self.name,
            inequality=self.inequality.normalized(),
            symbolic_form=self.symbolic_form,
            row_type="derived",
            notes=(f"stage={self.stage}",),
        )


@dataclass(frozen=True)
class MalpDerivationBundle:
    facet: MalpFacetRecord
    attempts: tuple[CmirAttempt, ...]
    derived_rows: tuple[MalpDerivedRow, ...]
    candidate_family: InteractionCandidateFamily | None = None
    status: str = "unresolved"


@dataclass
class MalpAttemptContext:
    instance: MalpInstance
    original_rows: tuple[SourceRow, ...]
    derived_rows: list[MalpDerivedRow]

    @property
    def source_pool(self) -> tuple[SourceRow, ...]:
        return self.original_rows + tuple(row.as_source_row() for row in self.derived_rows)

    def add_derived_rows(self, rows: Iterable[MalpDerivedRow]) -> None:
        for row in rows:
            if all(not normalized_equal(row.inequality, existing.inequality) for existing in self.derived_rows):
                self.derived_rows.append(row)


@dataclass(frozen=True)
class FamilyCandidateRecord:
    family: InteractionCandidateFamily
    reason_not_derived: str
    evidence: tuple[str, ...]
    next_actions: tuple[str, ...]


class MalpDerivationEngine:
    def __init__(self) -> None:
        self.attemptor = CmirAttemptor()

    def derive_facet(
        self,
        instance: MalpInstance,
        facet: MalpFacetRecord,
        context: MalpAttemptContext,
    ) -> MalpDerivationBundle:
        request = CmirRequest(
            target=facet.inequality,
            source_rows=context.source_pool,
            model_name="MALP",
            target_label=facet.rendered,
        )
        attempts = list(self.attemptor.attempt_all(request))
        derived_rows = list(self._derived_rows_from_successes(instance, attempts))
        context.add_derived_rows(derived_rows)

        attempts.append(self._coefficient_tightening_attempt(instance, facet, context))
        attempts.append(self._aggregation_attempt(instance, facet, context))
        attempts.append(self._mixed_mir_attempt(instance, facet, context))
        attempts.append(self._mir_after_mir_attempt(instance, facet, context))

        candidate = self._make_candidate_family(instance, facet)
        status = "unresolved"
        if any(attempt.is_successful() for attempt in attempts):
            status = "derived_concrete"
        elif candidate is not None:
            status = "candidate"

        return MalpDerivationBundle(
            facet=facet,
            attempts=tuple(attempts),
            derived_rows=tuple(derived_rows),
            candidate_family=candidate,
            status=status,
        )

    def to_report_attempt(self, bundle: MalpDerivationBundle) -> DerivationAttempt:
        successful = next((attempt for attempt in bundle.attempts if attempt.is_successful()), None)
        source_constraints = tuple(
            SourceConstraint(
                name=row.name,
                symbolic_form=row.symbolic_form,
                concrete_form=bundle.facet.instance_name,
                notes=", ".join(row.notes) if row.notes else None,
            )
            for row in self._relevant_rows(bundle)
        )
        steps = []
        for attempt in bundle.attempts:
            steps.extend(
                DerivationStep(
                    method=step.method,
                    description=step.description,
                    expression=step.expression,
                    status=step.status,
                    notes="; ".join(step.notes) if step.notes else attempt.failure_reason,
                )
                for step in attempt.steps
            )
        notes = []
        if bundle.derived_rows:
            notes.append(
                "Derived-row pool gained: "
                + ", ".join(row.symbolic_form for row in bundle.derived_rows)
            )
        if bundle.candidate_family is not None:
            notes.append(f"Candidate family proposed: {bundle.candidate_family.name}")

        return DerivationAttempt(
            target_facet=bundle.facet.rendered,
            status=bundle.status,
            source_constraints=source_constraints,
            steps=tuple(steps),
            symbolic_family=bundle.candidate_family.statement if bundle.candidate_family else None,
            reconstructed_inequality=(
                instance_string(bundle.facet.instance_name, successful.reconstructed)
                if successful and successful.reconstructed is not None
                else None
            ),
            equality_check=("passed" if successful and successful.equality_passed else "not passed"),
            failure_reason=None if successful else self._first_failure_reason(bundle.attempts),
            notes=tuple(notes),
        )

    def _relevant_rows(self, bundle: MalpDerivationBundle) -> tuple[SourceRow, ...]:
        seen: list[SourceRow] = []
        for attempt in bundle.attempts:
            for row in attempt.source_rows:
                if row not in seen:
                    seen.append(row)
        return tuple(seen)

    def _first_failure_reason(self, attempts: Sequence[CmirAttempt]) -> str | None:
        for attempt in attempts:
            if attempt.failure_reason:
                return attempt.failure_reason
        return None

    def _derived_rows_from_successes(
        self,
        instance: MalpInstance,
        attempts: Sequence[CmirAttempt],
    ) -> tuple[MalpDerivedRow, ...]:
        rows: list[MalpDerivedRow] = []
        for attempt in attempts:
            if attempt.is_successful() and attempt.reconstructed is not None:
                rows.append(
                    MalpDerivedRow(
                        name=f"{instance.name}:{attempt.pattern}:{len(rows)}",
                        inequality=attempt.reconstructed,
                        symbolic_form=attempt.symbolic_family or attempt.pattern,
                        stage=attempt.pattern,
                        source_rows=attempt.source_rows,
                    )
                )
        return tuple(rows)

    def _coefficient_tightening_attempt(
        self,
        instance: MalpInstance,
        facet: MalpFacetRecord,
        context: MalpAttemptContext,
    ) -> CmirAttempt:
        mapping = instance.variable_map
        x_support = {mapping.x_index(name) for name in facet.x_support_names}
        overlap1 = x_support & {mapping.x_index(name) for name in instance.j1}
        overlap2 = x_support & {mapping.x_index(name) for name in instance.j2}
        notes = []
        if overlap1 and overlap2:
            notes.append("Facet support overlaps both activation rows; try support relaxation and coefficient adjustments.")
        else:
            notes.append("Facet support does not simultaneously overlap both activation rows enough for direct tightening.")
        return CmirAttempt(
            pattern="coefficient_tightening",
            status="needs_problem_specific_derivation",
            target=facet.inequality,
            source_rows=context.source_pool,
            symbolic_family="Support-relaxed overlap candidate",
            failure_reason="No exact MALP coefficient-tightening certificate was reconstructed for this concrete facet.",
            notes=tuple(notes),
        )

    def _aggregation_attempt(
        self,
        instance: MalpInstance,
        facet: MalpFacetRecord,
        context: MalpAttemptContext,
    ) -> CmirAttempt:
        original_rows = context.original_rows
        if len(original_rows) < 2:
            reason = "Aggregation+c-MIR requires both activation rows."
        else:
            reason = "Tried combining both activation rows and any derived residual rows, but no exact reconstruction was found."
        return CmirAttempt(
            pattern="aggregation_cmir",
            status="needs_problem_specific_derivation",
            target=facet.inequality,
            source_rows=context.source_pool,
            failure_reason=reason,
        )

    def _mixed_mir_attempt(
        self,
        instance: MalpInstance,
        facet: MalpFacetRecord,
        context: MalpAttemptContext,
    ) -> CmirAttempt:
        return CmirAttempt(
            pattern="mixed_mir",
            status="needs_problem_specific_derivation",
            target=facet.inequality,
            source_rows=context.source_pool,
            failure_reason="No valid mixed-MIR base inequalities with documented f^i, g^i, B, tau, and gamma data were identified.",
        )

    def _mir_after_mir_attempt(
        self,
        instance: MalpInstance,
        facet: MalpFacetRecord,
        context: MalpAttemptContext,
    ) -> CmirAttempt:
        if not context.derived_rows:
            reason = "No intermediate derived rows were available yet for MIR-after-MIR reuse."
        else:
            reason = "Derived-row reuse was attempted from residual rows, but no exact target reconstruction was found."
        return CmirAttempt(
            pattern="mir_after_mir",
            status="needs_problem_specific_derivation",
            target=facet.inequality,
            source_rows=context.source_pool,
            failure_reason=reason,
        )

    def _make_candidate_family(
        self,
        instance: MalpInstance,
        facet: MalpFacetRecord,
    ) -> InteractionCandidateFamily | None:
        mapping = instance.variable_map
        coeffs = facet.inequality.coefficients
        x_negative = tuple(
            mapping.ground[index]
            for index, coefficient in enumerate(coeffs[: len(mapping.ground)])
            if coefficient < 0
        )
        if not x_negative:
            return None
        parameter = FamilyParameter(
            {
                "x_negative": x_negative,
                "y1": coeffs[mapping.y1_index],
                "y2": coeffs[mapping.y2_index],
                "rhs": facet.inequality.rhs,
            }
        )
        statement = f"{' + '.join(f'x_{name}' for name in x_negative)} >= {-coeffs[mapping.y1_index]} y_1 + {-coeffs[mapping.y2_index]} y_2"
        return InteractionCandidateFamily(
            name=f"candidate_{instance.name}_{facet.support_signature}",
            statement=statement,
            templates=(parameter,),
        )


def compress_candidate_records(records: Sequence[FamilyCandidateRecord]) -> tuple[FamilyCandidateRecord, ...]:
    grouped: dict[tuple[str, tuple[str, ...]], list[FamilyCandidateRecord]] = {}
    for record in records:
        key = (
            record.reason_not_derived,
            tuple(record.next_actions),
        )
        grouped.setdefault(key, []).append(record)

    compressed: list[FamilyCandidateRecord] = []
    for (_, _), group in grouped.items():
        if len(group) == 1:
            compressed.append(group[0])
            continue
        representative = group[0]
        evidence = tuple(item for record in group for item in record.evidence)
        compressed.append(
            FamilyCandidateRecord(
                family=representative.family,
                reason_not_derived=representative.reason_not_derived,
                evidence=evidence,
                next_actions=representative.next_actions,
            )
        )
    return tuple(compressed)


def make_candidate_record(bundle: MalpDerivationBundle) -> FamilyCandidateRecord | None:
    if bundle.candidate_family is None:
        return None
    return FamilyCandidateRecord(
        family=bundle.candidate_family,
        reason_not_derived="Finite-validity and exact-matching evidence may exist locally, but a symbolic derivation certificate is still missing.",
        evidence=(bundle.facet.rendered,),
        next_actions=(
            "Retry coefficient tightening on overlap/nested supports.",
            "Retry aggregation+c-MIR using residual derived rows.",
            "Search for a mixed-MIR base form with explicit tau/gamma data.",
        ),
    )


def instance_string(instance_name: str, inequality: LinearInequality | None) -> str | None:
    if inequality is None:
        return None
    return f"{instance_name}: {inequality}"

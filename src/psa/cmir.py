from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Literal

from psa.inequality import LinearInequality


PatternName = Literal[
    "residual",
    "coefficient_tightening",
    "aggregation_cmir",
    "mixed_mir",
    "mir_after_mir",
    "custom",
]

AttemptStatus = Literal[
    "derived",
    "candidate",
    "attempted",
    "failed",
    "needs_problem_specific_derivation",
    "not_applicable",
]


@dataclass(frozen=True)
class VariableInfo:
    """Metadata about one variable.

    This is intentionally lightweight. Problem-specific adapters may add
    richer metadata outside this class.
    """

    index: int
    name: str
    kind: str = "binary"
    lower_bound: int | float | None = 0
    upper_bound: int | float | None = 1


@dataclass(frozen=True)
class SourceRow:
    """A source inequality available for c-MIR-style derivation attempts.

    Inequalities use the project's LinearInequality convention.

    For activation lower-bound rows of the form

        x(J) >= b y,

    the normalized <= form is

        -x(J) + b y <= 0.

    To enable the generic residual attempt, provide:

    - row_type = "activation_lower"
    - x_support = indices of J
    - y_index = index of y
    - threshold = b
    """

    name: str
    inequality: LinearInequality
    symbolic_form: str
    row_type: str = "generic"
    x_support: tuple[int, ...] = ()
    y_index: int | None = None
    threshold: int | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CmirStep:
    """One documented step in a c-MIR derivation attempt."""

    method: str
    description: str
    expression: str | None = None
    status: str | None = None
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CmirAttempt:
    """A structured attempt to derive one target facet."""

    pattern: PatternName
    status: AttemptStatus
    target: LinearInequality
    source_rows: tuple[SourceRow, ...] = ()
    steps: tuple[CmirStep, ...] = ()
    reconstructed: LinearInequality | None = None
    equality_passed: bool = False
    symbolic_family: str | None = None
    parameter_conditions: tuple[str, ...] = ()
    failure_reason: str | None = None
    notes: tuple[str, ...] = ()

    def is_successful(self) -> bool:
        return self.status == "derived" and self.equality_passed


@dataclass(frozen=True)
class CmirRequest:
    """Input for deriving one concrete target facet."""

    target: LinearInequality
    source_rows: tuple[SourceRow, ...]
    variables: tuple[VariableInfo, ...] = ()
    model_name: str | None = None
    target_label: str | None = None


CustomPatternHandler = Callable[[CmirRequest], Sequence[CmirAttempt]]


@dataclass
class CmirAttemptor:
    """Generic c-MIR derivation attemptor.

    This class is not a complete theorem prover.

    It performs deterministic easy checks and produces structured derivation
    attempts for harder c-MIR patterns. Problem-specific adapters should call
    this attemptor first, then add model-specific attempts when needed.
    """

    custom_handlers: list[CustomPatternHandler] = field(default_factory=list)

    def register(self, handler: CustomPatternHandler) -> None:
        self.custom_handlers.append(handler)

    def attempt_all(self, request: CmirRequest) -> tuple[CmirAttempt, ...]:
        attempts: list[CmirAttempt] = []

        attempts.extend(self.attempt_residual(request))
        attempts.append(self.attempt_coefficient_tightening(request))
        attempts.append(self.attempt_aggregation_cmir(request))
        attempts.append(self.attempt_mixed_mir(request))
        attempts.append(self.attempt_mir_after_mir(request))

        for handler in self.custom_handlers:
            attempts.extend(handler(request))

        return tuple(attempts)

    def attempt_residual(self, request: CmirRequest) -> tuple[CmirAttempt, ...]:
        """Try the residual pattern against all activation lower-bound rows.

        Pattern:

            x(J) >= b y
            D subset J
            x(D) >= (b - |J \\ D|) y

        In <= convention:

            -x(D) + (b - |J \\ D|) y <= 0.
        """
        attempts: list[CmirAttempt] = []

        for row in request.source_rows:
            if row.row_type != "activation_lower":
                continue

            if row.y_index is None or row.threshold is None or not row.x_support:
                attempts.append(
                    self._failed(
                        "residual",
                        request.target,
                        (row,),
                        "Activation lower-bound row is missing x_support, y_index, or threshold metadata.",
                    )
                )
                continue

            attempt = self._attempt_residual_from_row(request.target, row)
            attempts.append(attempt)

        if not attempts:
            attempts.append(
                CmirAttempt(
                    pattern="residual",
                    status="not_applicable",
                    target=request.target.normalized(),
                    failure_reason="No activation_lower source row was provided.",
                    steps=(
                        CmirStep(
                            method="residual",
                            description="Residual pattern requires a source row of the form x(J) >= b y.",
                            status="not_applicable",
                        ),
                    ),
                )
            )

        return tuple(attempts)

    def _attempt_residual_from_row(
        self,
        target: LinearInequality,
        row: SourceRow,
    ) -> CmirAttempt:
        normalized_target = target.normalized()

        if normalized_target.sense != "<=":
            return self._failed(
                "residual",
                normalized_target,
                (row,),
                "Residual attempt currently expects target in <= convention.",
            )

        if normalized_target.rhs != 0:
            return self._failed(
                "residual",
                normalized_target,
                (row,),
                "Residual target must have right-hand side 0 in the current implementation.",
            )

        coefficients = normalized_target.coefficients
        y_index = row.y_index
        assert y_index is not None
        threshold = row.threshold
        assert threshold is not None

        source_support = set(row.x_support)
        negative_unit_x_support: list[int] = []
        nonzero_outside: list[int] = []

        for index, coefficient in enumerate(coefficients):
            if index == y_index:
                continue
            if coefficient == -1 and index in source_support:
                negative_unit_x_support.append(index)
            elif coefficient != 0:
                nonzero_outside.append(index)

        if nonzero_outside:
            return self._failed(
                "residual",
                normalized_target,
                (row,),
                "Target contains nonzero coefficients outside the selected source row and activation variable.",
            )

        target_y_coefficient = coefficients[y_index]
        subset = tuple(sorted(negative_unit_x_support))
        residual = threshold - (len(source_support) - len(subset))

        reconstructed_coeffs = [0] * len(coefficients)
        for index in subset:
            reconstructed_coeffs[index] = -1
        reconstructed_coeffs[y_index] = residual

        reconstructed = LinearInequality(
            tuple(reconstructed_coeffs),
            0,
            "<=",
        ).normalized()

        if residual <= 0:
            return CmirAttempt(
                pattern="residual",
                status="not_applicable",
                target=normalized_target,
                source_rows=(row,),
                reconstructed=reconstructed,
                equality_passed=False,
                failure_reason="Residual coefficient is nonpositive.",
                steps=(
                    CmirStep(
                        method="residual",
                        description="Computed residual coefficient b - |J \\ D|.",
                        expression=f"{threshold} - ({len(source_support)} - {len(subset)}) = {residual}",
                        status="not_applicable",
                    ),
                ),
            )

        equality_passed = reconstructed == normalized_target

        if equality_passed:
            return CmirAttempt(
                pattern="residual",
                status="derived",
                target=normalized_target,
                source_rows=(row,),
                reconstructed=reconstructed,
                equality_passed=True,
                symbolic_family="Residual family: x(D) >= (b - |J \\ D|) y",
                parameter_conditions=(
                    "D subset J",
                    "b - |J \\ D| > 0",
                ),
                steps=(
                    CmirStep(
                        method="source",
                        description="Start from activation lower-bound row.",
                        expression=row.symbolic_form,
                    ),
                    CmirStep(
                        method="residual",
                        description="Let D be the target x-support and use upper bounds on J \\ D.",
                        expression="x(D) >= (b - |J \\ D|) y",
                    ),
                    CmirStep(
                        method="exact_matching",
                        description="The reconstructed residual inequality matches the normalized target facet.",
                        status="passed",
                    ),
                ),
            )

        return CmirAttempt(
            pattern="residual",
            status="failed",
            target=normalized_target,
            source_rows=(row,),
            reconstructed=reconstructed,
            equality_passed=False,
            failure_reason=(
                "Residual reconstruction did not exactly match the target facet. "
                f"Target y coefficient is {target_y_coefficient}; residual coefficient is {residual}."
            ),
            steps=(
                CmirStep(
                    method="residual",
                    description="Computed residual coefficient b - |J \\ D|.",
                    expression=f"{threshold} - ({len(source_support)} - {len(subset)}) = {residual}",
                    status="failed",
                ),
            ),
        )

    def attempt_coefficient_tightening(self, request: CmirRequest) -> CmirAttempt:
        relevant_rows = self._rows_overlapping_target(request)

        return CmirAttempt(
            pattern="coefficient_tightening",
            status="needs_problem_specific_derivation",
            target=request.target.normalized(),
            source_rows=relevant_rows,
            failure_reason=(
                "Generic coefficient tightening requires model-specific choices of subsets, "
                "bounds, and coefficients. A problem adapter should try the documented "
                "coefficient-tightening pattern and record the pre-tightening and "
                "post-tightening inequalities."
            ),
            steps=(
                CmirStep(
                    method="coefficient_tightening",
                    description="Identify source rows and target support.",
                    status="attempted",
                ),
                CmirStep(
                    method="coefficient_tightening",
                    description="Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.",
                    status="needs_problem_specific_derivation",
                ),
            ),
        )

    def attempt_aggregation_cmir(self, request: CmirRequest) -> CmirAttempt:
        relevant_rows = self._rows_overlapping_target(request)

        return CmirAttempt(
            pattern="aggregation_cmir",
            status="needs_problem_specific_derivation",
            target=request.target.normalized(),
            source_rows=relevant_rows,
            failure_reason=(
                "Generic aggregation+c-MIR requires choosing multipliers and identifying "
                "the integer and bounded parts of the aggregate. This must be provided "
                "by a problem-specific adapter or a more specialized pattern handler."
            ),
            steps=(
                CmirStep(
                    method="source_identification",
                    description="Collected source rows whose supports overlap the target facet.",
                    status="attempted",
                ),
                CmirStep(
                    method="aggregation_cmir",
                    description="Choose nonnegative multipliers, aggregate rows, then apply c-MIR.",
                    status="needs_problem_specific_derivation",
                ),
            ),
        )

    def attempt_mixed_mir(self, request: CmirRequest) -> CmirAttempt:
        relevant_rows = self._rows_overlapping_target(request)

        return CmirAttempt(
            pattern="mixed_mir",
            status="needs_problem_specific_derivation",
            target=request.target.normalized(),
            source_rows=relevant_rows,
            failure_reason=(
                "Mixed MIR is not ordinary aggregation. The adapter must provide base "
                "inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, "
                "compute tau_i and gamma_i, identify a common dominating bar_f, "
                "and simplify the mixed-MIR inequality."
            ),
            steps=(
                CmirStep(
                    method="mixed_mir",
                    description="Try to put source rows into valid mixed-MIR base-inequality form.",
                    status="needs_problem_specific_derivation",
                ),
                CmirStep(
                    method="mixed_mir",
                    description="If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.",
                    status="needs_problem_specific_derivation",
                ),
            ),
        )

    def attempt_mir_after_mir(self, request: CmirRequest) -> CmirAttempt:
        relevant_rows = self._rows_overlapping_target(request)

        return CmirAttempt(
            pattern="mir_after_mir",
            status="needs_problem_specific_derivation",
            target=request.target.normalized(),
            source_rows=relevant_rows,
            failure_reason=(
                "MIR-after-MIR requires one or more previously derived valid inequalities "
                "to be used as new source rows. The generic attemptor does not invent "
                "these rows automatically."
            ),
            steps=(
                CmirStep(
                    method="mir_after_mir",
                    description="Search for previously derived valid inequalities that can serve as new source rows.",
                    status="needs_problem_specific_derivation",
                ),
            ),
        )

    def _rows_overlapping_target(self, request: CmirRequest) -> tuple[SourceRow, ...]:
        target_support = set(request.target.normalized().support)

        rows: list[SourceRow] = []
        for row in request.source_rows:
            row_support = set(row.inequality.normalized().support)
            if row_support & target_support:
                rows.append(row)

        return tuple(rows)

    def _failed(
        self,
        pattern: PatternName,
        target: LinearInequality,
        source_rows: tuple[SourceRow, ...],
        reason: str,
    ) -> CmirAttempt:
        return CmirAttempt(
            pattern=pattern,
            status="failed",
            target=target.normalized(),
            source_rows=source_rows,
            failure_reason=reason,
            steps=(
                CmirStep(
                    method=pattern,
                    description=reason,
                    status="failed",
                ),
            ),
        )


def successful_attempts(attempts: Iterable[CmirAttempt]) -> tuple[CmirAttempt, ...]:
    return tuple(attempt for attempt in attempts if attempt.is_successful())


def unresolved_attempts(attempts: Iterable[CmirAttempt]) -> tuple[CmirAttempt, ...]:
    return tuple(
        attempt
        for attempt in attempts
        if attempt.status in {"failed", "needs_problem_specific_derivation", "attempted"}
    )


def convert_activation_lower_row(
    *,
    name: str,
    inequality: LinearInequality,
    symbolic_form: str,
    x_support: Sequence[int],
    y_index: int,
    threshold: int,
    notes: Sequence[str] = (),
) -> SourceRow:
    """Convenience constructor for rows of the form x(J) >= b y."""
    return SourceRow(
        name=name,
        inequality=inequality.normalized(),
        symbolic_form=symbolic_form,
        row_type="activation_lower",
        x_support=tuple(x_support),
        y_index=y_index,
        threshold=threshold,
        notes=tuple(notes),
    )
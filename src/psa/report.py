from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field

from psa.inequality import LinearInequality


@dataclass(frozen=True)
class ConcreteFacetReference:
    """Reference to a computed concrete facet used as evidence.

    This object should be used only as supporting evidence for a symbolic
    family. It should not drive the main report structure.
    """

    inequality: str
    source: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class InequalityFamily:
    """A symbolic inequality family discovered from computed facets."""

    name: str
    statement: str
    derivation: Sequence[str] | str
    validity_status: str
    facetness_status: str = "unproved"
    completeness_status: str = "not claimed"
    conditions: Sequence[str] = field(default_factory=tuple)
    covered_facets: Sequence[ConcreteFacetReference | str] = field(default_factory=tuple)
    notes: Sequence[str] = field(default_factory=tuple)


@dataclass(frozen=True)
class CoverageSummary:
    """Compact evidence that a symbolic family explains computed facets."""

    family: str
    covered_facets: int
    sources: Sequence[str] = field(default_factory=tuple)
    notes: str = ""


@dataclass(frozen=True)
class UnmatchedFacet:
    """A computed facet that has not yet been explained by a symbolic family."""

    inequality: str
    source: str | None = None
    reason: str = "no symbolic derivation found"


def format_inequality(
    inequality: LinearInequality,
    variable_names: tuple[str, ...],
) -> str:
    terms: list[str] = []

    for coefficient, name in zip(inequality.coefficients, variable_names, strict=True):
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
    return f"{lhs} {inequality.sense} {inequality.rhs}"


def render_family_discovery_report(
    *,
    title: str,
    model_description: str,
    families: Sequence[InequalityFamily | Mapping],
    coverage: Sequence[CoverageSummary | Mapping] = (),
    unmatched_facets: Sequence[UnmatchedFacet | Mapping] = (),
    proof_obligations: Sequence[str] = (),
    scope_notes: Sequence[str] = (),
    appendix: Sequence[str] = (),
) -> str:
    """Render a family-first discovery report.

    The report is organized by symbolic inequality families rather than by
    computational instances. Concrete facets may appear only as evidence,
    coverage, unmatched items, or appendix material.

    Parameters
    ----------
    title:
        Report title.
    model_description:
        General mathematical description of the studied set or model.
    families:
        Symbolic inequality families with derivations and status labels.
    coverage:
        Compact evidence showing which computed facets are explained by each
        family.
    unmatched_facets:
        Computed facets that are not yet explained by symbolic derivations.
    proof_obligations:
        Remaining mathematical tasks.
    scope_notes:
        Optional limitations or methodological notes.
    appendix:
        Optional appendix lines. Use this for raw computational evidence only.
    """
    normalized_families = [_as_family(family) for family in families]
    normalized_coverage = [_as_coverage(item) for item in coverage]
    normalized_unmatched = [_as_unmatched_facet(item) for item in unmatched_facets]

    lines = [
        f"# {title}",
        "",
        "## Scope and limitations",
        "",
    ]

    if scope_notes:
        for note in scope_notes:
            lines.append(f"- {note}")
    else:
        lines.extend(
            [
                "- This report uses computed facets as evidence for symbolic inequality families.",
                "- Concrete instance-level inequalities are not treated as the final output.",
                "- No complete convex-hull description is claimed unless a reverse-inclusion proof is provided.",
            ]
        )

    lines.extend(
        [
            "",
            "## Model",
            "",
            model_description.strip(),
            "",
            "## Derived symbolic inequality families",
            "",
        ]
    )

    if normalized_families:
        for family in normalized_families:
            lines.extend(_render_family(family))
    else:
        lines.append("No symbolic inequality family has been derived yet.")
        lines.append("")

    lines.extend(
        [
            "## Coverage of computed facets",
            "",
            "This section records computational evidence showing which concrete facets are explained by the symbolic families above.",
            "It is not a proof of completeness.",
            "",
        ]
    )
    lines.extend(_render_coverage(normalized_coverage))

    lines.extend(["", "## Unmatched computed facets", ""])
    if normalized_unmatched:
        lines.append(
            "The following computed facets have not yet been explained by a symbolic derivation."
        )
        lines.append("")
        for facet in normalized_unmatched:
            lines.extend(_render_unmatched_facet(facet))
    else:
        lines.append("No unmatched computed facets were reported.")

    lines.extend(["", "## Proof obligations", ""])
    if proof_obligations:
        for index, obligation in enumerate(proof_obligations, start=1):
            lines.append(f"{index}. {obligation}")
    else:
        lines.extend(
            [
                "1. Prove validity of every symbolic inequality family for all admissible parameters.",
                "2. For each derived family, record a complete aggregation, c-MIR, lifting, or bound-substitution certificate.",
                "3. Determine the parameter regimes in which each family is facet-defining.",
                "4. Check whether all computed nontrivial facets are covered by the reported symbolic families.",
                "5. Do not claim a complete convex hull description until reverse inclusion is proved.",
            ]
        )

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "The current output is a family-discovery report. It presents symbolic inequality families and their derivation status, using computed facets only as evidence. It does not by itself constitute a complete convex-hull description.",
        ]
    )

    if appendix:
        lines.extend(["", "## Appendix: computational evidence", ""])
        lines.append(
            "The appendix may contain raw computational evidence. It is not the main mathematical output."
        )
        lines.append("")
        lines.extend(appendix)

    return "\n".join(lines) + "\n"


def _render_family(family: InequalityFamily) -> list[str]:
    lines = [
        f"### {family.name}",
        "",
        "#### Symbolic statement",
        "",
        family.statement.strip(),
        "",
    ]

    if family.conditions:
        lines.extend(["#### Parameter conditions", ""])
        for condition in family.conditions:
            lines.append(f"- {condition}")
        lines.append("")

    lines.extend(["#### Derivation certificate", ""])
    if isinstance(family.derivation, str):
        lines.append(family.derivation.strip())
    else:
        for step in family.derivation:
            lines.append(f"- {step}")
    lines.append("")

    lines.extend(
        [
            "#### Status",
            "",
            f"- validity: `{family.validity_status}`",
            f"- facetness: `{family.facetness_status}`",
            f"- completeness: `{family.completeness_status}`",
            "",
        ]
    )

    if family.covered_facets:
        lines.extend(["#### Covered computed facets", ""])
        for facet in family.covered_facets:
            lines.extend(_render_concrete_facet_reference(facet))
        lines.append("")

    if family.notes:
        lines.extend(["#### Notes", ""])
        for note in family.notes:
            lines.append(f"- {note}")
        lines.append("")

    return lines


def _render_concrete_facet_reference(
    facet: ConcreteFacetReference | str,
) -> list[str]:
    if isinstance(facet, str):
        return [f"- {facet}"]

    line = f"- `{facet.inequality}`"
    details = []
    if facet.source:
        details.append(f"source: {facet.source}")
    if facet.notes:
        details.append(facet.notes)
    if details:
        line += f" ({'; '.join(details)})"
    return [line]


def _render_coverage(coverage: Sequence[CoverageSummary]) -> list[str]:
    if not coverage:
        return ["No coverage data was provided.", ""]

    lines = [
        "| family | covered facets | evidence sources | notes |",
        "| --- | ---: | --- | --- |",
    ]

    for item in coverage:
        sources = ", ".join(item.sources) if item.sources else ""
        lines.append(
            f"| {item.family} | {item.covered_facets} | {sources} | {item.notes} |"
        )

    lines.append("")
    return lines


def _render_unmatched_facet(facet: UnmatchedFacet) -> list[str]:
    lines = [f"- inequality: `{facet.inequality}`"]
    if facet.source:
        lines.append(f"  - source: {facet.source}")
    lines.append(f"  - reason: {facet.reason}")
    return lines


def _as_family(value: InequalityFamily | Mapping) -> InequalityFamily:
    if isinstance(value, InequalityFamily):
        return value

    return InequalityFamily(
        name=str(value["name"]),
        statement=str(value["statement"]),
        derivation=value["derivation"],
        validity_status=str(value["validity_status"]),
        facetness_status=str(value.get("facetness_status", "unproved")),
        completeness_status=str(value.get("completeness_status", "not claimed")),
        conditions=tuple(str(item) for item in value.get("conditions", ())),
        covered_facets=tuple(_as_concrete_facet(item) for item in value.get("covered_facets", ())),
        notes=tuple(str(item) for item in value.get("notes", ())),
    )


def _as_concrete_facet(value: ConcreteFacetReference | str | Mapping) -> ConcreteFacetReference | str:
    if isinstance(value, ConcreteFacetReference | str):
        return value

    return ConcreteFacetReference(
        inequality=str(value["inequality"]),
        source=str(value["source"]) if value.get("source") is not None else None,
        notes=str(value["notes"]) if value.get("notes") is not None else None,
    )


def _as_coverage(value: CoverageSummary | Mapping) -> CoverageSummary:
    if isinstance(value, CoverageSummary):
        return value

    return CoverageSummary(
        family=str(value["family"]),
        covered_facets=int(value.get("covered_facets", 0)),
        sources=tuple(str(item) for item in value.get("sources", ())),
        notes=str(value.get("notes", "")),
    )


def _as_unmatched_facet(value: UnmatchedFacet | Mapping) -> UnmatchedFacet:
    if isinstance(value, UnmatchedFacet):
        return value

    return UnmatchedFacet(
        inequality=str(value["inequality"]),
        source=str(value["source"]) if value.get("source") is not None else None,
        reason=str(value.get("reason", "no symbolic derivation found")),
    )
from __future__ import annotations

from collections.abc import Iterable

from psa.inequality import LinearInequality


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


def render_malp_initial_report(results: list[dict], candidate_families: list[dict]) -> str:
    lines = [
        "# MALP initial facet study",
        "",
        "## Scope and limitations",
        "",
        "This report studies small MALP instances by exhaustive 0-1 point enumeration and convex-hull computation with the current cdd backend.",
        "No complete convex-hull claim is made. Any family not directly derived from the original constraints is labeled as experimentally supported or conjectural unless a proof is provided.",
        "",
        "## MALP set",
        "",
        "We study",
        "",
        "`T = { (x, y1, y2) in {0,1}^{|J1 ∪ J2| + 2} : x(J1) >= b1 y1, x(J2) >= b2 y2 }`.",
        "",
        "For each instance we use the variable order `(x over J1 ∪ J2 in sorted index order, y1, y2)`.",
        "We also use the partition `A = J1 \\ J2`, `B = J2 \\ J1`, `C = J1 ∩ J2`.",
        "",
        "## Instance catalog",
        "",
        "| instance | relation | J1 | J2 | b1 | b2 | dim | feasible points |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for result in results:
        instance = result["instance"]
        lines.append(
            f"| {result['name']} | {instance.relation_type()} | {instance.j1} | {instance.j2} | {instance.b1} | {instance.b2} | {instance.dimension} | {len(result['points'])} |"
        )

    for result in results:
        instance = result["instance"]
        variable_names = instance.variable_names()
        lines.extend(
            [
                "",
                f"## {result['name']}",
                "",
                f"- relation: `{instance.relation_type()}`",
                f"- J1 = `{instance.j1}`",
                f"- J2 = `{instance.j2}`",
                f"- b = `({instance.b1}, {instance.b2})`",
                f"- partition: `A={instance.a_only}`, `B={instance.b_only}`, `C={instance.overlap}`",
                f"- feasible 0-1 points: `{len(result['points'])}`",
                "",
                "### Variable bounds",
                "",
            ]
        )
        lines.extend(_render_inequality_bullets(result["variable_bounds"], variable_names))

        lines.extend(["", "### Original constraints appearing in the computed hull", ""])
        if result["original_constraints"]:
            lines.extend(_render_inequality_bullets(result["original_constraints"], variable_names))
        else:
            lines.append("- none; the computed hull is represented by stronger inequalities for this instance")

        if result["missing_original_constraints"]:
            lines.extend(["", "### Original constraints not appearing verbatim in the computed hull", ""])
            lines.extend(
                _render_inequality_bullets(
                    result["missing_original_constraints"],
                    variable_names,
                )
            )
            lines.append("- note: these remain valid original model constraints, but the hull output is using stronger inequalities instead of listing them verbatim")

        lines.extend(["", "### Nontrivial candidate inequalities", ""])
        if result["nontrivial_candidates"]:
            lines.extend(
                _render_inequality_bullets(
                    result["nontrivial_candidates"],
                    variable_names,
                )
            )
        else:
            lines.append("- none observed beyond bounds and the original constraints")

    lines.extend(["", "## Cross-instance candidate families", ""])

    if candidate_families:
        for family in candidate_families:
            lines.extend(
                [
                    f"### {family['name']}",
                    "",
                    f"- status: `{family['status']}`",
                    f"- observed in: {', '.join(family['instances'])}",
                    f"- template: `{family['template']}`",
                    f"- note: {family['note']}",
                    "",
                ]
            )
    else:
        lines.append("No recurring nontrivial family was detected across the tested instances.")

    lines.extend(
        [
            "## Proof obligations",
            "",
            "1. Prove validity of every experimentally supported family for general admissible `(J1, J2, b1, b2)`.",
            "2. Determine the exact parameter regimes in which each nontrivial family is necessary.",
            "3. Prove or disprove facetness for each nontrivial family before calling it a facet family.",
            "4. Check whether the tested hull inequalities are fully covered by the proposed family templates in each regime.",
            "5. If a complete hull system is ever proposed, prove reverse inclusion and state all assumptions and boundary cases.",
            "6. Cross-check the small instances with PORTA or another independent backend in a later study.",
            "",
            "## Conclusion",
            "",
            "The current results are an initial computational study only. They are useful for generating candidate inequalities and organizing proof obligations, but they do not constitute a complete convex-hull description of MALP.",
        ]
    )

    return "\n".join(lines) + "\n"


def _render_inequality_bullets(
    inequalities: Iterable[LinearInequality],
    variable_names: tuple[str, ...],
) -> list[str]:
    return [
        f"- `{format_inequality(inequality, variable_names)}`"
        for inequality in inequalities
    ]

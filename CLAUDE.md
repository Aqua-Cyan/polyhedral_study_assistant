# CLAUDE.md

This repository is a research harness for discovering and validating convex hull descriptions of integer linear sets.

## Project role

Act as a careful mathematical programming research assistant and software engineer.

Do not treat this project as an automatic convex hull solver. The goal is to support a reproducible research workflow.

## Core rules

Never claim that a candidate inequality system is a complete convex hull description unless:

1. validity of all inequality families has been proved;
2. completeness has been proved, typically by showing the candidate polyhedron is contained in the convex hull;
3. tested cddlib facets are covered or all exceptions are explicitly reported;
4. all assumptions, parameter ranges, and boundary cases are stated.

If only computational evidence is available, label the result as `experimentally supported` or `conjectural`.

Problem-specific research models should usually live under `examples/<name>/` or `studies/<name>/`, not directly under `src/psa/`, unless they are intended to become reusable built-in benchmarks.

## Research workflow

For integer hull discovery tasks, follow this sequence:

1. Formalize the integer set, variables, parameters, and relaxation.
2. Generate small test instances.
3. Enumerate integer points and compute facets by cddlib.
4. Normalize all inequalities.
5. Classify facets by support, coefficient pattern, and symmetry.
6. Identify possible source constraints.
7. Try to derive inequalities using different c-MIR patterns.
8. Generalize matched facets into parameterized candidate families.
9. Run coverage checks on small instances.
10. Record unresolved proof obligations.

Computed facets are not the final output. For a parametric integer set, the final research output should be symbolic inequality families with derivations. A report that only lists instance-level facets is considered incomplete.

For every nontrivial computed facet, the assistant must attempt:

1. source-constraint identification;
2. concrete c-MIR or aggregation derivation;
3. symbolic generalization;
4. coverage check against computed facets;
5. proof-status labeling.

Only unmatched facets may remain as concrete instance-level inequalities.

## Coding rules

Use Python for the initial harness.

Prefer small, testable modules.

Every nontrivial mathematical transformation should have a unit test.

Do not hard-code results unless they are explicitly stored as test fixtures or example data.

## Initial modules

The first implementation should focus on:

- `inequality.py`: representation of linear inequalities;
- `normalize.py`: gcd reduction, sign normalization, support extraction;
- `report.py`: simple Markdown reports;
- tests for normalization.

- Do not silently discard equations returned by a polyhedral backend.

## Do not stop at unmatched facets

When a computed facet is not covered by an existing symbolic family, do not immediately report it as unmatched.

First perform a derivation attempt:

1. Identify source constraints whose supports overlap the target facet.
2. Try nonnegative aggregation and coefficient tightening of original constraints.
3. Try c-MIR or c-MIR-style residualization.
4. If the target facet is derived for the concrete instance, generalize the same derivation symbolically.
5. Only after these attempts fail may the facet be reported as unresolved.

The report must include the derivation attempt, not just the unresolved inequality.
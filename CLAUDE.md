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

## Candidate family validation pipeline

When studying a parametric integer set, computed facets are evidence, not final mathematical output.

The required pipeline is:

computed cdd facets -> facet normalization -> candidate family proposal -> Gate 1: instantiation matching -> Gate 2: finite validity check -> Gate 3: derivation certificate check -> family-first report.

Gate 1: instantiation matching

A symbolic family may not claim to cover a computed facet unless the following check is performed:

instantiate the symbolic family on the concrete test instance and chosen family parameters;
generate the concrete LinearInequality;
normalize the instantiated inequality;
normalize the computed cdd facet;
check exact equality.

Do not count a facet as covered by visual similarity or informal pattern resemblance. If exact normalized equality fails, the facet is not covered by that family.

Gate 2: finite validity check

Every candidate family instance must be checked on all enumerated feasible 0-1 points of the corresponding small instance.

If a feasible point violates the instantiated inequality, the family instance must be placed in Invalidated candidate families.

The report must include:

concrete instance;
family parameter values;
instantiated inequality;
violating feasible point;
violation value if available.

An invalidated family must not appear as a derived or proved family.

Gate 3: derivation certificate check

A candidate family may be reported as derived or proved valid only if it has a derivation certificate using documented patterns, such as:

residual inequality;
coefficient tightening;
aggregation;
c-MIR;
mixed MIR;
sequential MIR or MIR applied after MIR.

The certificate must record:

source constraints;
substitutions or bounds used;
intermediate inequalities;
rounding, MIR, or mixing step if used;
final symbolic inequality;
equality check between reconstructed inequality and the computed facet when claiming coverage.

A family that passes finite tests but lacks a derivation certificate must be labeled as candidate, not proved valid.

Candidate refinement loop:

For every proposed candidate family:

instantiate it on all tested small instances;
check exact matching against cdd facets;
check finite validity on all enumerated feasible 0-1 points;
if invalid, produce a counterexample and ask how to refine the conditions;
if valid on tests but no derivation exists, keep it in Candidate symbolic inequality families;
try to derive it using the documented c-MIR patterns;
only after a derivation certificate exists may it move to Derived or proved symbolic inequality families.

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
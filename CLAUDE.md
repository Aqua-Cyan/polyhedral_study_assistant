# CLAUDE.md

This repository is a research harness for discovering and validating convex hull descriptions of integer linear sets.

## Project role

Act as a careful mathematical programming research assistant and software engineer.

Do not treat this project as an automatic convex hull solver. The goal is to support a reproducible research workflow.

## Core rules

Never claim that a candidate inequality system is a complete convex hull description unless:

1. validity of all inequality families has been proved;
2. completeness has been proved, typically by showing the candidate polyhedron is contained in the convex hull;
3. tested PORTA facets are covered or all exceptions are explicitly reported;
4. all assumptions, parameter ranges, and boundary cases are stated.

If only computational evidence is available, label the result as `experimentally supported` or `conjectural`.

## Research workflow

For integer hull discovery tasks, follow this sequence:

1. Formalize the integer set, variables, parameters, and relaxation.
2. Generate small test instances.
3. Compute or import PORTA facets.
4. Normalize all inequalities.
5. Classify facets by support, coefficient pattern, and symmetry.
6. Identify possible source constraints.
7. Try to derive inequalities using aggregation and c-MIR.
8. Generalize matched facets into parameterized candidate families.
9. Run coverage checks on small instances.
10. Record unresolved proof obligations.

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
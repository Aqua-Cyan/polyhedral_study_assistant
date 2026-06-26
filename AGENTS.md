# AGENTS.md

This repository develops a Python research harness for polyhedral studies in integer programming.

## Main objective

Build reliable tools for:

- representing and normalizing linear inequalities;
- enumerating 0-1 feasible points;
- computing convex-hull inequalities with cddlib (via pycddlib);
- classifying and clustering facet-defining inequalities;
- matching computed facets against candidate symbolic inequality families;
- recording c-MIR / mixed-MIR / MIR-over-MIR derivation certificates;
- running a regulator-controlled research loop that dispatches tasks to AI agents;
- producing reproducible, machine-readable reports and state files.

## Development priorities

1. Correctness over speed.
2. Explicit mathematical assumptions.
3. Small modules with tests.
4. Clear JSON/Markdown outputs.
5. No unsupported claims about complete convex hull descriptions.

## Architecture

### Generic layer (`src/psa/`)

| Module | Purpose |
|---|---|
| `inequality.py` | `LinearInequality` representation |
| `normalize.py` | Inequality normalization |
| `binary_points.py` | 0-1 point enumeration |
| `backends/` | cddlib backend wrappers |
| `cmir.py` | c-MIR, mixed MIR, MIR-over-MIR |
| `derivation.py` | Derivation-attempt records |
| `family.py` | Family

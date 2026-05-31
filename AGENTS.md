# AGENTS.md

This repository develops a Python research harness for polyhedral studies in integer programming.

## Main objective

Build reliable tools for:

- representing linear inequalities;
- normalizing inequalities;
- parsing and organizing PORTA outputs;
- matching computed facets against candidate inequality families;
- producing reproducible reports.

## Development priorities

1. Correctness over speed.
2. Explicit mathematical assumptions.
3. Small modules with tests.
4. Clear JSON/Markdown outputs.
5. No unsupported claims about complete convex hull descriptions.

## Commands

After the Python package is initialized, use:

```bash
python -m pytest
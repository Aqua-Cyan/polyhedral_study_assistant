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
| `family.py` | Family protocol, family memory, exact matching |
| `validity.py` | Finite validity checking |
| `report.py` | Report and state utilities |
| `agent/state.py` | `ResearchState`, state/task-pool loading |
| `agent/regulator.py` | `SingleRegulator` — deterministic task selection |
| `agent/prompt_builder.py` | Role-specific prompt generation for Claude Code |
| `agent/executors.py` | `ClaudeCodeExecutor` — CLI runner |

### Problem-specific layer (`examples/<problem_id>/`)

Each problem adapter contains:

- `README.md` — problem definition
- `model.py` — variables, feasibility, instance generation
- `families.py` — candidate family templates
- `derive.py` — problem-specific derivation attempts
- `study.py` — `run(max_union_size: int) -> dict` entry point

### Scripts

- `scripts/study.py` — one-shot study adapter runner
- `scripts/psa_loop.py` — regulated research-loop runner

## Commands

### Install

```bash
pip install -e .
```

### Run tests

```bash
python -m pytest
```

### One-shot study

```bash
python scripts/study.py --problem malp --max-size 5
```

### Regulated loop (manual)

```bash
python scripts/psa_loop.py --problem malp --max-size 5
```

### Regulated loop (automatic)

```bash
python scripts/psa_loop.py --problem malp --max-size 5 --execute --rounds 10
```

## Regulator decision chain

The `SingleRegulator` uses a deterministic priority chain:

1. `CREATE_ADAPTER` — no `examples/<problem_id>/study.py` exists; generate adapter from README.
2. `RUN_STUDY_FIRST` — no state file exists.
3. `VERIFY_FAMILY_GUESS` — unverified guess JSON exists (highest priority).
4. `DONE` — `candidate_count == 0` and `unresolved_count == 0`.
5. `BLOCKED_NO_CONCRETE_TASKS` — no open concrete tasks.
6. Task selection: `derive_family`/`implement_family`/`revise_guess` → `family_compression` (when `candidate_count >= 20`) → `derive_interaction_family` → `analyze_unresolved_signature` → fallback.

## Agent roles

- **FamilyGuesser** — proposes symbolic families from facet clusters; writes to `memory/family/<problem_id>/guesses/`.
- **Verifier** — checks guesses; writes to `memory/family/<problem_id>/verifications/`; verdicts: `accept_for_implementation`, `needs_revision`, `invalid`, `insufficient`.
- **DerivationProver** — derives families from source constraints using c-MIR patterns; produces derivation certificates.
- **StudyAdapter** — runs the computational study and updates all artifacts.

## Status labels

Use conservative labels: `raw cddlib facet`, `candidate`, `local candidate`, `invalidated`, `experimentally supported`, `derived`, `proved valid`, `facetness unproved`, `complete hull not claimed`, `unresolved`.

Do not use `derived` without a derivation certificate. Do not use `complete` without a completeness proof.

## Code-change rules

1. Keep generic utilities in `src/psa/`.
2. Keep problem-specific logic in `examples/<problem_id>/`.
3. Add or update tests when changing behavior.
4. Rerun tests or study scripts after code changes.
5. Do not silently change status labels to stronger claims.

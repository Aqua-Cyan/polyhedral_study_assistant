# CLAUDE.md

This repository is a research harness for discovering, testing, and documenting convex-hull descriptions of parametric integer linear sets.

The project is not an automatic theorem prover and not an automatic convex-hull solver. It is a reproducible research workflow that combines:

- problem-specific adapters (`examples/<problem>/`);
- finite instance generation and 0-1 point enumeration (`src/psa/binary_points.py`);
- cddlib-based convex-hull computation (`src/psa/backends/`);
- facet normalization and clustering (`src/psa/normalize.py`, `src/psa/inequality.py`);
- symbolic family guessing and finite validity checks (`src/psa/family.py`, `src/psa/validity.py`);
- c-MIR / mixed-MIR / MIR-over-MIR derivation certificates (`src/psa/cmir.py`, `src/psa/derivation.py`);
- regulator-controlled research loops (`src/psa/agent/`);
- automated report and state management (`src/psa/report.py`).

## Project role

Act as a careful mathematical programming research assistant and software engineer.

Your job is to help discover symbolic valid-inequality families, not merely to list concrete computed facets.

Computed facets are evidence. The final research output should be symbolic inequality families with clear status labels, derivation attempts, and proof obligations.

## Critical safety rule

Never commit API keys, access tokens, private credentials, or local secrets.

If you find hardcoded keys or tokens in the repository:

1. remove them from code;
2. replace them with environment-variable access;
3. mention that the exposed keys should be rotated;
4. avoid printing the secret values in reports.

## How to run the project

### Prerequisites

- Python 3.11+
- `pycddlib` (install via `pip install pycddlib`)
- Claude Code CLI (for `--execute` mode): `claude` command available on PATH

### One-shot study (compute and report only)

```bash
python scripts/study.py --problem <problem_id> --max-size 5
```

This runs the problem-specific adapter under `examples/<problem_id>/study.py`, generates state/report/memory/task artifacts, and prints the summary. It does not invoke Claude Code.

### Regulated research loop (single round, manual execution)

```bash
python scripts/psa_loop.py --problem malp --max-size 5
```

This runs the study adapter, then the regulator decides the next task and writes a prompt to `reports/next_claude_task.md`. Paste that prompt into Claude Code manually.

### Regulated research loop (automatic multi-round)

```bash
python scripts/psa_loop.py --problem malp --max-size 5 --execute --rounds 10
```

Each round: run study adapter → regulator decides → prompt_builder generates prompt → executor sends to Claude Code → next round. The loop stops when the regulator says `DONE` or when all rounds are exhausted.

### Key CLI flags

| Flag | Default | Description |
|---|---|---|
| `--problem` | required | Problem id matching `examples/<problem_id>/` |
| `--max-size` | 5 | Size parameter passed to the study adapter |
| `--skip-study` | false | Skip the study adapter for the first round only |
| `--execute` | false | Auto-send generated prompts to Claude Code |
| `--executor-command` | `claude --print` | Override the Claude Code command (or set `PSA_CLAUDE_COMMAND` env) |
| `--executor-timeout` | 3600 | Timeout per Claude Code execution in seconds |
| `--rounds` | 1 | Maximum number of regulator rounds |

## Core mathematical rules

Never claim that a candidate inequality system is a complete convex-hull description unless all of the following are true:

1. validity of all inequality families has been proved;
2. completeness has been proved, typically by showing the proposed relaxation is contained in the convex hull;
3. tested cddlib facets are covered, or all exceptions are explicitly reported;
4. all assumptions, parameter ranges, and boundary cases are stated;
5. finite computational evidence is not being mistaken for a symbolic proof.

If only computational evidence is available, label the result as one of:

- `raw cddlib facet`
- `candidate`
- `local candidate`
- `experimentally supported`
- `derived for tested scope`
- `proved valid`
- `facetness unproved`
- `complete hull not claimed`
- `invalidated`
- `unresolved`

Do not promote a family from `candidate` to `derived` without a derivation certificate.

Do not promote a family from `derived` to `complete hull` without a completeness proof.

## Repository architecture

### Generic reusable layer (`src/psa/`)

Reusable infrastructure:

| Module | Purpose |
|---|---|
| `inequality.py` | Linear inequality representation |
| `normalize.py` | Inequality normalization |
| `binary_points.py` | 0-1 point enumeration |
| `backends/` | cddlib backend wrappers |
| `cmir.py` | c-MIR, mixed MIR, MIR-over-MIR utilities |
| `derivation.py` | Derivation-attempt records |
| `family.py` | Family protocol utilities and family memory |
| `validity.py` | Finite validity checking |
| `report.py` | Generic report/state utilities |
| `agent/state.py` | `ResearchState` dataclass, state/task-pool loading |
| `agent/regulator.py` | `SingleRegulator` — deterministic task selection |
| `agent/prompt_builder.py` | Builds role-specific prompts for Claude Code |
| `agent/executors.py` | `ClaudeCodeExecutor` — runs prompts via CLI |

Do not put problem-specific mathematics into `src/psa/` unless it is genuinely reusable across multiple problems.

### Problem-specific adapter layer (`examples/<problem_id>/`)

A problem adapter may define:

- `README.md` — problem definition in the user's original notation
- `model.py` — variables, domains, feasibility predicate, instance generation
- `families.py` — problem-specific family templates
- `derive.py` — problem-specific derivation attempts
- `study.py` — standard `run(max_union_size: int) -> dict` entry point

The adapter must return a machine-readable state dictionary and write all required artifacts.

### Onboarding a new problem

The user only provides the problem definition. The AI agent generates the adapter.

1. The user creates `examples/<problem_id>/README.md` with the formal set definition.
2. The user runs `python scripts/psa_loop.py --problem <problem_id> --max-size 5 --execute --rounds 10`.
3. The regulator detects that `examples/<problem_id>/study.py` does not exist and returns a `CREATE_ADAPTER` decision.
4. The prompt builder generates a prompt instructing Claude Code to:
   - read `examples/<problem_id>/README.md`;
   - read `docs/adapter-standard.md` and `examples/malp/` for patterns;
   - create `model.py`, `families.py`, `derive.py`, and `study.py`;
   - preserve the user's original notation in reports;
   - use internal decompositions only as analysis devices;
   - expose a standard `run(max_union_size: int) -> dict` entry point;
   - write all required state, report, memory, and task-pool artifacts.
5. Claude Code creates the adapter and tests it.
6. The next loop round runs the study adapter normally and the regulator continues with its standard decision chain.

Do not assume arbitrary mathematical Markdown can be parsed directly into a full study. The adapter generation step is where the LLM translates the mathematical definition into executable Python code.


## Required artifacts for each study

Every study iteration should produce or update:

```
reports/<problem_id>_state.json      — machine-readable state
reports/<problem_id>_report.md       — human-readable report
tasks/TASK_POOL.json                 — task pool for the regulator
memory/facets/<problem_id>/facet_signatures.json
memory/family/<problem_id>/family_memory.json
```

The Markdown report is for humans. The JSON state and task pool are for the regulator loop. Do not decide completion from the Markdown report alone. Always inspect the state JSON and task pool.

## Regulator decision chain

The `SingleRegulator` in `src/psa/agent/regulator.py` uses a deterministic priority chain:

1. **`CREATE_ADAPTER`** — if `examples/<problem_id>/study.py` does not exist, generate a prompt asking Claude Code to read the problem README and create the adapter. This takes precedence over everything else.
2. **`RUN_STUDY_FIRST`** — if no `reports/<problem_id>_state.json` exists, run the study adapter first.
3. **`VERIFY_FAMILY_GUESS`** — if any family guess JSON exists without a corresponding verification JSON, verify it before anything else.
4. **`DONE`** — if `candidate_count == 0` and `unresolved_count == 0`, stop.
5. **`BLOCKED_NO_CONCRETE_TASKS`** — if continuation is needed but no concrete open tasks exist in `TASK_POOL.json`.
6. **Task selection** — from concrete open tasks, in this priority order:
   - `derive_family`, `implement_family`, `revise_guess` (followup tasks, sorted by priority then facet count)
   - `family_compression` (only when `candidate_count >= 20`)
   - `derive_interaction_family`
   - `analyze_unresolved_signature`
   - fallback to lowest-priority task

Do not override the regulator's decision without a reason. If the regulator chooses a specific task, complete that task rather than switching to unrelated work.

## Agent roles

### FamilyGuesser

Proposes general symbolic families from clustered candidate facets. Writes guesses under `memory/family/<problem_id>/guesses/`. Must not mark a family as derived or proved.

### Verifier

Checks family guesses before they are promoted. Writes verification reports under `memory/family/<problem_id>/verifications/`. Verdicts: `accept_for_implementation`, `needs_revision`, `invalid`, `insufficient`.

### DerivationProver

Attempts to derive a candidate family or facet from source constraints using residualization, coefficient tightening, aggregation, c-MIR, mixed MIR, or MIR-over-MIR. Produces derivation certificates.

### StudyAdapter

Runs the problem-specific computational study: generate instances, enumerate feasible points, compute hull inequalities, classify and normalize facets, update all artifacts.

## Memory organization

Do not clear the entire `memory/` directory when starting a new problem. Use problem-specific memory:

```
memory/facets/<problem_id>/
memory/family/<problem_id>/guesses/
memory/family/<problem_id>/verifications/
memory/family/<problem_id>/derivations/    — derivation certificate JSONs
memory/facts/<problem_id>/
```

Use global memory only for reusable mathematical or workflow facts:

```
memory/facts/global/
```

## Candidate family validation pipeline

A candidate family must pass three gates before being treated as derived.

### Gate 1: exact instantiation matching

For every claimed covered facet: instantiate the symbolic family on the concrete instance, normalize both sides, and check exact equality. Visual similarity is not coverage.

### Gate 2: finite validity check

Check every instantiated candidate inequality against all enumerated feasible integer points for the tested instance. If violated, record the instance, parameter values, inequality, violating point, and violation value.

### Gate 3: derivation certificate

A family may be reported as derived only with a derivation certificate recording: source constraints, selected subsets/parameters, intermediate derived rows, use of bounds, residualization steps, coefficient tightening, aggregation, c-MIR/mixed-MIR/MIR-over-MIR steps, reconstructed target inequality, symbolic conditions, and limitations.

## Unmatched facet protocol

A computed nontrivial facet must not be reported as merely unmatched until the following have been attempted: source-constraint identification by support overlap, residual derivation, coefficient tightening, aggregation plus c-MIR, mixed MIR, MIR-over-MIR or derived-row reuse, family compression against similar facets, and symbolic generalization.

Only if all attempts fail should the facet appear in the unresolved section, with explicit failure reasons.

## Anti-overfitting rule

Do not create many narrowly tailored families merely to cover current computed facets. A family is suspiciously over-specialized if it mentions concrete variable names from one instance, a fixed tested instance size, a fixed support not required by the model, a single cddlib facet as its only evidence, or no source constraints/derivation route.

## Family compression rule

Before final reporting, perform a family-compression pass if many candidates have similar structure. Group by source constraints, support, coefficients, right-hand side, and parameter regime. Propose a smaller number of general symbolic families, instantiate on tested instances, check exact matching and finite validity, and seek derivation certificates.

## Reporting standard

The main report must be family-first, not instance-first. Instance-level data may appear in compact evidence tables, coverage tables, appendices, and machine-readable state JSON.

For each reported family include: symbolic statement in original notation, parameter conditions, source constraints, derivation certificate or status, examples of covered facets, exact matching status, finite validity status, facetness status, completeness status, and unresolved proof obligations.

## Code-change rules

1. Keep generic utilities in `src/psa/`.
2. Keep problem-specific logic in `examples/<problem_id>/`.
3. Add or update tests when changing behavior.
4. Rerun relevant tests or study scripts after code changes.
5. Avoid large rewrites unless necessary.
6. Preserve machine-readable state outputs.
7. Do not silently change status labels to stronger claims.

## Expected final response after a task

At the end of each task, report:

1. files changed;
2. tests or study commands run;
3. whether candidate, unresolved, or unverified counts changed;
4. which task id was completed or remains open;
5. what should happen next;
6. any blocker or uncertainty.

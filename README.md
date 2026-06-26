# polyhedral_study_assistant

`polyhedral_study_assistant` is a research harness for studying convex-hull descriptions of parametric integer linear sets. It combines finite-instance computation, symbolic family discovery, derivation certificates, and a regulator-controlled loop that orchestrates AI-assisted research iterations.

The goal is not to automatically solve arbitrary convex-hull problems. Instead, this project helps researchers:

- generate and manage small integer programming instances;
- compute small-instance convex hulls using cddlib (via pycddlib);
- normalize and classify facet-defining inequalities;
- match computed facets against candidate symbolic inequality families;
- record c-MIR / mixed-MIR / MIR-over-MIR derivation certificates;
- track proof obligations for proposed convex-hull descriptions;
- run a regulator that decides the next research task and dispatches it to an AI agent.

## Intended users

Researchers in integer programming, polyhedral combinatorics, and combinatorial optimization who want a reproducible, machine-readable workflow for discovering and validating valid-inequality families.

## Prerequisites

- **Python 3.11+**
- **pycddlib** — install with `pip install pycddlib`
- **Claude Code CLI** (optional, for `--execute` mode) — the `claude` command must be available on your PATH

Install Python dependencies:

```bash
pip install -e .
```

This installs the `psa` package and its dependencies (including pycddlib) from `pyproject.toml`.

## Project structure

```
polyhedral_study_assistant/
├── src/psa/                    # Generic reusable infrastructure
│   ├── inequality.py           #   linear inequality representation
│   ├── normalize.py            #   inequality normalization
│   ├── binary_points.py        #   0-1 point enumeration
│   ├── backends/               #   cddlib backend wrappers
│   ├── cmir.py                 #   c-MIR, mixed MIR, MIR-over-MIR
│   ├── derivation.py           #   derivation-attempt records
│   ├── family.py               #   family protocol utilities
│   ├── validity.py             #   finite validity checking
│   ├── report.py               #   report/state utilities
│   └── agent/                  #   regulator-controlled loop
│       ├── state.py            #     ResearchState, state loading
│       ├── regulator.py        #     SingleRegulator (task selection)
│       ├── prompt_builder.py   #     role-specific prompt generation
│       └── executors.py        #     ClaudeCodeExecutor (CLI runner)
├── examples/                   # Problem-specific adapters
│   └── malp/                   #   worked example: multi-activation lower bound
│       ├── README.md           #     problem definition
│       ├── model.py            #     variables, feasibility, instance generation
│       ├── families.py         #     candidate family templates
│       ├── derive.py           #     problem-specific derivation attempts
│       └── study.py            #     run(max_union_size) -> dict entry point
├── scripts/                    # Entry-point scripts
│   ├── study.py                #   one-shot study adapter runner
│   └── psa_loop.py             #   regulated research-loop runner
├── docs/                       # Documentation and templates
├── memory/                     # Research memory (per-problem and global)
├── reports/                    # Generated reports and state files
├── tasks/                      # TASK_POOL.json for the regulator
├── tests/                      # Unit tests
├── ai/skills/SKILL.md          # Optional skill prompt for AI agents
├── CLAUDE.md                   # Project-level instructions for Claude Code
├── AGENTS.md                   # Agent-oriented project summary
└── pyproject.toml              # Package configuration
```

## Quick start

### 1. Run a one-shot study

Compute facets for the built-in `malp` example and generate all artifacts:

```bash
python scripts/study.py --problem malp --max-size 5
```

This will:

- load the adapter from `examples/malp/study.py`
- generate staged finite instances up to size 5
- enumerate feasible 0-1 points
- compute convex-hull inequalities with cddlib
- normalize and classify facets
- write `reports/malp_state.json`, `reports/malp_report.md`, `tasks/TASK_POOL.json`, and memory files
- print a summary of candidate, unresolved, and derived record counts

### 2. Run the regulated research loop (manual mode)

Generate the next Claude Code task without executing it:

```bash
python scripts/psa_loop.py --problem malp --max-size 5
```

This runs the study adapter, then the regulator examines the state and writes a prompt to `reports/next_claude_task.md`. You then paste that prompt into Claude Code manually.

### 3. Run the regulated research loop (automatic mode)

Let the loop dispatch tasks to Claude Code automatically for up to 10 rounds:

```bash
python scripts/psa_loop.py --problem malp --max-size 5 --execute --rounds 10
```

Each round:

1. The study adapter reruns and refreshes `reports/<problem_id>_state.json`.
2. The regulator reads the state and `tasks/TASK_POOL.json`, then selects the next task.
3. `prompt_builder.py` generates a role-specific prompt (FamilyGuesser, Verifier, or generic executor).
4. `executors.py` sends the prompt to Claude Code via `claude --print` (or your configured command).
5. The next round begins unless the regulator says `DONE` or all rounds are exhausted.

### 4. Check the results

After the loop completes, inspect:

| File | Contents |
|---|---|
| `reports/malp_state.json` | Machine-readable state: candidate counts, unresolved counts, derived counts, summary |
| `reports/malp_report.md` | Human-readable family-first report |
| `reports/regulator_decision.json` | Last regulator decision: selected task, next agent, stop flag |
| `reports/next_claude_task.md` | Last generated prompt (stable copy) |
| `tasks/TASK_POOL.json` | Open and completed research tasks |
| `memory/facets/malp/facet_signatures.json` | Normalized facet signatures |
| `memory/family/malp/family_memory.json` | Family memory: candidates, derived, unresolved |
| `memory/family/malp/guesses/` | Family guess JSONs from FamilyGuesser |
| `memory/family/malp/verifications/` | Verification reports from Verifier |
| `logs/claude/` | Archived prompts, stdout, stderr, and metadata from each round |

## CLI reference

### `scripts/study.py`

```
python scripts/study.py --problem <problem_id> [--max-size N]
```

| Flag | Default | Description |
|---|---|---|
| `--problem` | required | Problem id matching `examples/<problem_id>/` |
| `--max-size` | 5 | Size parameter passed to the adapter's `run()` |

### `scripts/psa_loop.py`

```
python scripts/psa_loop.py --problem <problem_id> [options]
```

| Flag | Default | Description |
|---|---|---|
| `--problem` | required | Problem id, e.g. `malp` |
| `--max-size` | 5 | Size parameter passed to `scripts/study.py` |
| `--skip-study` | false | Skip the study adapter for the first round only |
| `--execute` | false | Automatically send prompts to Claude Code |
| `--executor-command` | `claude --print` | Override the Claude CLI command (or set `PSA_CLAUDE_COMMAND`) |
| `--executor-timeout` | 3600 | Timeout in seconds per Claude Code execution |
| `--rounds` | 1 | Maximum number of regulator rounds |

## Adding a new problem

1. **Define the problem.** Create `examples/<your_problem>/README.md` with the formal set definition, variables, domains, and parameters.

2. **Create the adapter.** Write `examples/<your_problem>/study.py` exposing:

   ```python
   def run(max_union_size: int = 5) -> dict:
       ...
   ```

   The adapter must return a state dictionary and write all required artifacts (state JSON, report, task pool, memory files). You can split logic into `model.py`, `families.py`, and `derive.py` as needed.

3. **Create `__init__.py` files.** Ensure `examples/__init__.py` and `examples/<your_problem>/__init__.py` exist (they can be empty).

4. **Test the adapter.**

   ```bash
   python scripts/study.py --problem <your_problem> --max-size 5
   ```

5. **Run the full loop.**

   ```bash
   python scripts/psa_loop.py --problem <your_problem> --max-size 5 --execute --rounds 10
   ```

## Configuration

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `PSA_CLAUDE_COMMAND` | `claude --print` | Default Claude CLI command used by the executor |

Copy `.env.example` to `.env` and adjust as needed. The executor passes the prompt via stdin by default. If your CLI expects a file path instead, use a command template with `{prompt_file}`:

```bash
python scripts/psa_loop.py --problem malp --execute --executor-command "claude --print {prompt_file}"
```

## Running tests

```bash
python -m pytest
```

## Philosophy

A candidate inequality system should not be called a complete convex-hull description unless:

- every inequality family has a validity proof;
- tested cddlib facets are covered or exceptions are explained;
- the reverse inclusion has been proved;
- all assumptions and parameter ranges are explicit.

Computed facets are evidence. The final output should be symbolic inequality families with derivation certificates, not raw facet lists.
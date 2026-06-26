---
name: integer-hull-discovery
description: Analyze parametric integer linear sets, discover convex-hull inequalities via cddlib, derive valid inequalities with c-MIR, classify facet families, and run regulator-controlled research loops.
---

# Integer Hull Discovery

This skill supports research workflows for parametric integer linear sets.

Use staged computational evidence, symbolic family discovery, derivation certificates, finite validation, and regulator-controlled iteration. Do not guess a complete convex-hull description directly.

## When to use this skill

Activate this skill when the task involves:

- analyzing an integer linear set and its convex hull;
- interpreting cddlib-generated facet output;
- proposing or validating symbolic inequality families;
- deriving valid inequalities using c-MIR, mixed MIR, or MIR-over-MIR;
- building a problem-specific study adapter;
- running the regulator-controlled research loop (`scripts/psa_loop.py`).

Do not activate this skill for general optimization modeling, LP solving, or non-polyhedral tasks.

## Core principle

Computed facets are evidence, not the final mathematical output.

The final research output should be symbolic inequality families with:

- parameter conditions;
- source constraints;
- derivation certificates or explicit proof obligations;
- exact matching status;
- finite validity status;
- facetness status;
- completeness status.

Never call a description "the convex hull" unless validity and completeness are proved.

## Required workflow

### 1. Formalize the set

Define variables, domains, index sets, parameters, assumptions, possible overlap among index sets, feasibility assumptions, and the intended relaxation if any.

When a model is given in overlapping index-set notation, preserve the user's notation. You may use intersections, set differences, symmetry classes, or partitions internally, but label them as internal analysis devices.

### 2. Identify the intended goal

Clarify whether the user wants a complete convex-hull description, a valid inequality family, a facet family, a separation routine, an extended formulation, computational exploration, or a problem adapter for the research harness. Do not overclaim.

### 3. Create or use a problem adapter

The user provides only the problem definition in `examples/<problem_id>/README.md`. The AI agent generates the adapter automatically.

When the regulator detects that `examples/<problem_id>/study.py` does not exist, it returns a `CREATE_ADAPTER` decision. The prompt builder generates instructions for Claude Code to:

- read the README and `docs/adapter-standard.md`;
- create `model.py`, `families.py`, `derive.py`, and `study.py`;
- expose `run(max_union_size: int = 5) -> dict`;
- write all required artifacts.

The adapter must generate machine-readable research state and all required artifacts. After creation, the loop continues with the standard research workflow.

### 4. Generate staged finite instances

Use a staged instance plan: tiny sanity → small structured → medium → random/exhaustive sweeps → targeted edge cases.

For 0-1 sets, test enough variables to distinguish singleton supports, pair supports, proper subsets, full supports, overlaps, nested cases, and asymmetric thresholds.

### 5. Compute and normalize facets

For each finite instance: enumerate feasible integer points, compute convex-hull inequalities using cddlib, normalize every inequality, separate bounds/original constraints from nontrivial facets, and record support, coefficient pattern, and right-hand side.

### 6. Cluster facets

Group nontrivial facets by source constraints, support pattern, coefficient pattern, right-hand side pattern, active variables, symmetry class, and parameter regime.

### 7. Guess symbolic families

Turn repeated facet patterns into parameterized symbolic family candidates using arbitrary subsets (`D`), complements (`J \ D`), intersections, residual expressions (`b - |J \ D|`), threshold regimes, and candidate MIR structure.

Do not create one family per concrete facet unless no common structure exists.

### 8. Verify candidate families

A candidate family must pass three gates:

**Gate 1 — Exact instantiation matching:** instantiate the symbolic family on the finite instance, normalize both sides, check exact equality. Visual similarity is not coverage.

**Gate 2 — Finite validity check:** check instantiated inequalities against all enumerated feasible integer points. Record any violations with instance, parameters, inequality, violating point, and violation value.

**Gate 3 — Derivation certificate:** a family may be called derived only with a certificate recording source constraints, subsets/parameters, intermediate rows, bounds usage, residualization, coefficient tightening, aggregation, c-MIR/mixed-MIR/MIR-over-MIR steps, reconstructed inequality, symbolic conditions, and limitations.

### 9. Search for derivations

For every nontrivial facet or candidate family, attempt: source-constraint identification, residual derivation, coefficient tightening, aggregation plus c-MIR, mixed MIR, MIR-over-MIR or derived-row reuse, family compression, and symbolic generalization.

Only after all attempts fail may a facet be placed in `unresolved` status.

### 10. Report honestly

Use conservative labels: `raw cddlib facet`, `candidate`, `local candidate`, `invalidated`, `experimentally supported`, `derived`, `proved valid`, `facetness unproved`, `complete hull not claimed`, `unresolved`.

## Regulator-controlled loop

The project includes a deterministic regulator in `src/psa/agent/regulator.py`. The main entry point is `scripts/psa_loop.py`.

### Regulator priority chain

1. **`CREATE_ADAPTER`** — no `examples/<problem_id>/study.py` exists; generate adapter from README.
2. **`RUN_STUDY_FIRST`** — no state file exists yet.
3. **`VERIFY_FAMILY_GUESS`** — any guess JSON without a matching verification JSON; this takes precedence over all other tasks.
4. **`DONE`** — `candidate_count == 0` and `unresolved_count == 0`.
5. **`BLOCKED_NO_CONCRETE_TASKS`** — continuation needed but no open concrete tasks.
6. **Task selection** — `derive_family`/`implement_family`/`revise_guess` first, then `family_compression` (when `candidate_count >= 20`), then `derive_interaction_family`, then `analyze_unresolved_signature`, then fallback.


### Running the loop

```bash
# Single round, manual prompt
python scripts/psa_loop.py --problem malp --max-size 5

# Automatic multi-round
python scripts/psa_loop.py --problem malp --max-size 5 --execute --rounds 10
```

Each round: study adapter runs → regulator decides → `prompt_builder.py` generates a role-specific prompt → `executors.py` sends it to Claude Code → next round.

### Key files read by the regulator

```
reports/<problem_id>_state.json
tasks/TASK_POOL.json
memory/facets/<problem_id>/
memory/family/<problem_id>/guesses/
memory/family/<problem_id>/verifications/
```

Do not override the regulator's decision. Complete the selected task as directed.

## Roles

### FamilyGuesser

Inspect candidate facet clusters, identify repeated patterns, propose a small number of general symbolic families. Write guess JSON under `memory/family/<problem_id>/guesses/`. Do not mark families as derived.

### Verifier

Read the guess JSON, check symbolic well-formedness, parameter explicitness, over-specialization, evidence plausibility, matching/validity implementability, and derivation route plausibility. Write verification JSON under `memory/family/<problem_id>/verifications/`. Verdicts: `accept_for_implementation`, `needs_revision`, `invalid`, `insufficient`.

### DerivationProver

Start from source constraints. Use residualization, coefficient tightening, aggregation, c-MIR, mixed MIR, or MIR-over-MIR. Produce a derivation certificate. Update family status only when all gates pass.

### StudyAdapter

Read `examples/<problem_id>/README.md`, create model/feasibility logic, generate instances, compute facets, classify and cluster, output all artifacts.

## Memory organization

Do not clear all memory when starting a new problem.

```
memory/facets/<problem_id>/
memory/family/<problem_id>/guesses/
memory/family/<problem_id>/verifications/
memory/family/<problem_id>/derivations/
memory/facts/<problem_id>/
memory/facts/global/      — reusable facts only
```

## Anti-overfitting rule

Do not introduce a symbolic family solely because it covers one computed facet in one small instance. A local candidate must remain local unless it appears across multiple instance sizes, is derived from source constraints, or is verified as a specialization of a broader family.

## Completion rule

The task is incomplete while any of the following remain:

- candidate families without derivation certificates;
- unresolved computed facets without failure chains;
- unverified family guesses;
- invalidated candidates not reflected in revised conditions;
- open high-priority task-pool items;
- missing exact matching checks;
- missing finite validity checks;
- missing derivation certificates for claimed derived families.

Stop only when the regulator permits stopping or a real blocker is reached. If blocked, report: completed work, unresolved items, blocker, and smallest next action.

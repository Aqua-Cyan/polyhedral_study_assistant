# Problem Adapter Standard

This document defines how a new problem-specific study should be added to the repository.

The repository should not try to parse arbitrary mathematical Markdown directly into a complete convex-hull study.

Instead, a user supplies a problem statement, and an LLM-assisted coding step creates a thin problem-specific adapter that conforms to the repository workflow.

## New problem location

A new problem should live under:

```text
examples/<problem_id>/
```

The user should define the set in:

```text
examples/<problem_id>/README.md
```

The README should state:

* variables;
* domains;
* index sets;
* parameters;
* assumptions;
* constraints;
* intended research goal;
* known regimes or boundary cases if available.

## Required adapter files

A problem adapter may contain:

```text
examples/<problem_id>/model.py
examples/<problem_id>/families.py
examples/<problem_id>/derive.py
examples/<problem_id>/study.py
```

Not every file is mandatory for very small examples, but `study.py` is required.

## Required study entry point

The adapter must expose a callable entry point.

Current standard:

```python
def run(max_union_size: int = 5) -> dict:
    ...
```

For problems where `max_union_size` is not meaningful, the adapter may interpret the size parameter differently, but it must document the interpretation.

The return value must be a machine-readable state dictionary.

## Required output artifacts

Running the adapter should update:

```text
reports/<problem_id>_state.json
reports/<problem_id>_report.md
tasks/TASK_POOL.json
memory/facets/<problem_id>/facet_signatures.json
memory/family/<problem_id>/family_memory.json
```

If family guesses or verifications are produced, they should be stored under:

```text
memory/family/<problem_id>/guesses/
memory/family/<problem_id>/verifications/
```

## What belongs in the adapter

Problem-specific code may include:

* canonical variable ordering;
* feasibility predicate;
* finite instance generation;
* source constraints;
* original inequalities;
* problem-specific candidate family templates;
* problem-specific derivation attempts;
* problem-specific notation formatting;
* problem-specific facet classification.

## What does not belong in the adapter

Do not reimplement generic infrastructure in each adapter.

The adapter should reuse generic code from `src/psa/` for:

* binary point enumeration when applicable;
* inequality representation;
* normalization;
* exact matching;
* finite validity checking;
* cdd backend calls;
* derivation-attempt data structures;
* report/state utilities when available;
* regulator orchestration.

If a utility becomes useful across multiple adapters, move it to `src/psa/`.

## State JSON requirements

The state file should include at least:

```json
{
  "problem_id": "...",
  "problem_name": "...",
  "state_version": 1,
  "tested_scope": {},
  "summary": {
    "instances": 0,
    "facets_total": 0,
    "derived_records": 0,
    "candidate_records": 0,
    "unresolved_records": 0,
    "signature_count": 0,
    "stop_status": "continue"
  },
  "instances": [],
  "derived_families": [],
  "candidate_facets": [],
  "unresolved_facets": [],
  "facet_signature_groups": [],
  "proof_obligations": []
}
```

The regulator depends on:

* `summary.candidate_records`;
* `summary.unresolved_records`;
* `summary.signature_count`;
* `summary.stop_status`;
* `facet_signature_groups`;
* `candidate_facets`;
* `unresolved_facets`.

Do not remove these fields without updating the regulator.

## Task pool requirements

The adapter should create or update:

```text
tasks/TASK_POOL.json
```

Tasks should be JSON objects with fields such as:

```json
{
  "id": "<problem_id>-family-compression-0001",
  "problem_id": "<problem_id>",
  "type": "family_compression",
  "status": "open",
  "priority": 1,
  "assigned_agent": "FamilyGuesser",
  "required_actions": [],
  "success_criterion": "..."
}
```

Recommended task types:

* `family_compression`;
* `derive_interaction_family`;
* `analyze_unresolved_signature`;
* `verify_family_guess`;
* `implement_family`;
* `derive_family`;
* `revise_guess`.

Avoid scheduling `regulator_decision` as a normal executor task. The regulator is implemented by Python and should not usually be delegated back to Claude Code.

## Status labels

Use conservative labels:

* `bound`;
* `original_constraint`;
* `raw cddlib facet`;
* `candidate`;
* `local candidate`;
* `invalidated`;
* `derived`;
* `proved valid`;
* `experimentally supported`;
* `unresolved`.

Do not use `derived` unless a derivation certificate exists.

Do not use `complete` unless a completeness proof exists.

## Exact matching requirement

If a family claims to cover a computed facet, the adapter should eventually support exact normalized matching:

1. instantiate the family;
2. normalize the instantiated inequality;
3. normalize the computed facet;
4. compare exact equality.

Visual similarity is not sufficient.

## Finite validity requirement

If a candidate family is instantiated on a finite test instance, it should eventually be checked on all enumerated feasible integer points for that instance.

A violated family must be recorded as invalidated.

## Derivation certificate requirement

A derived family should have a certificate recording:

* source constraints;
* subsets or parameters;
* intermediate rows;
* bounds used;
* residualization steps;
* coefficient tightening steps;
* aggregation;
* MIR or mixed-MIR steps;
* final symbolic statement;
* conditions and limitations.

## Family guessing and verification

FamilyGuesser writes guesses to:

```text
memory/family/<problem_id>/guesses/
```

Verifier writes reports to:

```text
memory/family/<problem_id>/verifications/
```

A guessed family remains a candidate until verified and derived.

## Memory layout

Do not mix problem-specific memory across problems.

Use:

```text
memory/facets/<problem_id>/
memory/family/<problem_id>/
memory/facts/<problem_id>/
```

Use:

```text
memory/facts/global/
```

only for reusable facts and workflow rules.

## Customer workflow

For a new customer problem:

1. create `examples/<problem_id>/README.md`;
2. run the generic study command;
3. if no adapter exists, ask the coding agent to generate one from the README;
4. run the adapter;
5. inspect the generated state and task pool;
6. let the regulator choose the next task.

The generic driver should not contain problem-specific mathematics.

Problem-specific mathematics belongs in the adapter.

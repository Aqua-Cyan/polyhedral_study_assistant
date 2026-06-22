---

name: integer-hull-discovery
description: Use this skill when analyzing integer linear sets, discovering convex-hull descriptions, interpreting cddlib-generated facets, deriving valid inequalities with c-MIR or mixed MIR, classifying facet families, building problem adapters, or running regulator-controlled integer-hull research loops.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Integer Hull Discovery

This skill supports research workflows for parametric integer linear sets.

Do not guess a complete convex-hull description directly.

Use staged computational evidence, symbolic family discovery, derivation certificates, finite validation, and regulator-controlled iteration.

## Core principle

Computed facets are evidence, not the final mathematical output.

The final research output should be symbolic inequality families with:

* parameter conditions;
* source constraints;
* derivation certificates or explicit proof obligations;
* exact matching status;
* finite validity status;
* facetness status;
* completeness status.

Never call a description "the convex hull" unless validity and completeness are proved.

## Required workflow

### 1. Formalize the set

Define:

* variables;
* domains;
* index sets;
* parameters;
* assumptions;
* possible overlap among index sets;
* feasibility assumptions;
* intended relaxation if any.

When a model is given in overlapping index-set notation, preserve the user's notation.

You may use intersections, set differences, symmetry classes, or partitions internally, but label them as internal analysis devices.

### 2. Identify the intended goal

Clarify whether the user wants:

* a complete convex-hull description;
* a valid inequality family;
* a facet family;
* a separation routine;
* an extended formulation;
* computational exploration;
* a problem adapter for the research harness.

Do not overclaim. If the current goal is computational exploration, do not present conjectures as theorems.

### 3. Create or use a problem adapter

A new problem should be placed under:

```text
examples/<problem_id>/
```

The user should define the model in:

```text
examples/<problem_id>/README.md
```

Do not assume arbitrary mathematical Markdown can be parsed directly into a full study.

Instead, create a thin problem-specific adapter containing:

* `model.py` if useful;
* `families.py` if useful;
* `derive.py` if useful;
* `study.py`.

The adapter must expose a callable study entry point, currently:

```python
def run(max_union_size: int = 5) -> dict:
    ...
```

The adapter must generate machine-readable research state.

### 4. Generate staged finite instances

Do not rely only on tiny examples.

Use a staged instance plan:

1. tiny sanity instances;
2. structured small instances;
3. medium structured instances;
4. random or exhaustive sweeps within feasible enumeration limits;
5. targeted edge cases for suspected missing families.

Include boundary regimes.

For 0-1 sets, test enough variables to distinguish:

* singleton supports;
* pair supports;
* proper subsets;
* full supports;
* overlaps;
* nested cases;
* asymmetric thresholds.

If computation is too expensive, state the bottleneck and use targeted structured cases.

### 5. Compute and normalize facets

For each finite instance:

1. enumerate feasible integer points;
2. compute convex-hull inequalities using the configured backend;
3. normalize every inequality;
4. separate variable bounds and original constraints from nontrivial facets;
5. record support, coefficient pattern, right-hand side, and source constraints.

### 6. Cluster facets

Group nontrivial facets by:

* source constraints;
* support pattern;
* coefficient pattern;
* right-hand side pattern;
* active variables;
* symmetry class;
* parameter regime.

These clusters are inputs to family discovery.

### 7. Guess symbolic families

Turn repeated facet patterns into parameterized symbolic family candidates.

Use:

* arbitrary subsets such as `D`;
* complements such as `J \ D`;
* intersections and set differences;
* residual expressions such as `b - |J \ D|`;
* threshold regimes;
* symmetry or ordering assumptions;
* candidate MIR or mixed-MIR structure.

Do not create one family per concrete facet unless no common structure exists.

A FamilyGuesser may propose candidates, but those candidates remain unproved.

### 8. Verify candidate families

A candidate family must pass these gates before being reported as derived.

#### Gate 1: exact instantiation matching

For every claimed covered computed facet:

1. instantiate the symbolic family on the finite instance;
2. normalize the instantiated inequality;
3. normalize the cddlib facet;
4. check exact equality.

Visual similarity is not coverage.

#### Gate 2: finite validity check

Check instantiated candidate inequalities against all enumerated feasible integer points for the tested instances.

If violated, record:

* concrete instance;
* parameter values;
* inequality;
* violating feasible point;
* violation value.

Invalid candidates must not be reported as derived.

#### Gate 3: derivation certificate check

A family may be called derived only with a derivation certificate.

The certificate should include:

* source constraints;
* selected subsets or parameters;
* intermediate rows;
* use of bounds;
* residualization;
* coefficient tightening;
* aggregation;
* c-MIR, mixed MIR, or MIR-over-MIR steps;
* final reconstructed inequality;
* symbolic conditions;
* limitations.

### 9. Search for derivations

For every nontrivial computed facet or candidate family, attempt:

1. source-constraint identification;
2. residual derivation;
3. coefficient tightening;
4. aggregation plus c-MIR;
5. mixed MIR;
6. MIR-over-MIR or derived-row reuse;
7. family compression;
8. symbolic generalization.

Only after these attempts fail may a facet be placed in unresolved status.

### 10. Report honestly

Use conservative labels:

* `raw cddlib facet`;
* `candidate`;
* `local candidate`;
* `invalidated`;
* `experimentally supported`;
* `derived`;
* `proved valid`;
* `facetness unproved`;
* `complete hull not claimed`;
* `unresolved`.

Never state that the hull is complete unless a proof is supplied.

## Regulator-controlled loop

When the repository has a regulator loop, do not work as if this is a one-shot prompt.

Read:

```text
reports/<problem_id>_state.json
tasks/TASK_POOL.json
memory/facets/<problem_id>/
memory/family/<problem_id>/
```

The regulator decides whether the next role is:

* `FamilyGuesser`;
* `Verifier`;
* `DerivationProver`;
* `StudyAdapter`;
* generic executor.

Follow the selected task.

Do not ignore `tasks/TASK_POOL.json`.

Do not declare completion if the state shows remaining candidate records, unresolved records, unverified guesses, or open high-priority tasks.

## Role: FamilyGuesser

Use this role when the regulator selects a family-compression or family-guessing task.

Responsibilities:

1. inspect candidate facet clusters;
2. identify repeated support and coefficient patterns;
3. propose a small number of general symbolic families;
4. avoid over-specialized local candidates;
5. write guess JSON files under:

```text
memory/family/<problem_id>/guesses/
```

Do not mark guessed families as derived.

A family guess should include:

* problem id;
* source task id;
* family id;
* symbolic statement;
* normalized template if applicable;
* parameters;
* parameter conditions;
* subsumed signatures;
* evidence facets;
* expected derivation route;
* validation plan;
* known risks.

## Role: Verifier

Use this role when the regulator selects a verification task for a family guess.

Responsibilities:

1. read the family guess JSON;
2. check that the statement is symbolic and well-formed;
3. check parameters and conditions;
4. check that it is not just a concrete facet with renamed variables;
5. check whether evidence facets match the template;
6. check whether exact instantiation matching is implementable;
7. check whether finite validity checking is implementable;
8. check whether the derivation route is plausible;
9. write verification JSON under:

```text
memory/family/<problem_id>/verifications/
```

The verifier verdict should be one of:

* `accept_for_implementation`;
* `needs_revision`;
* `invalid`;
* `insufficient`.

Do not strengthen a guess beyond the available evidence.

## Role: DerivationProver

Use this role when the regulator selects a derivation task.

Responsibilities:

1. identify source constraints;
2. derive concrete target inequalities when possible;
3. generalize concrete derivations to symbolic families;
4. record derivation certificates;
5. update family status only when gates are passed;
6. avoid invalid addition or overcounting;
7. try MIR-over-MIR or derived-row reuse for interaction facets.

## Role: StudyAdapter

Use this role when the regulator asks to create or update a problem-specific adapter.

Responsibilities:

1. read `examples/<problem_id>/README.md`;
2. preserve user notation in reports;
3. create problem-specific model and feasibility logic;
4. generate finite instances;
5. compute facets;
6. classify and cluster facets;
7. output report, state, task pool, and memory files.

## Required outputs

Unless the user asks for a different format, output sections should include:

1. Problem formalization;
2. Assumptions and edge cases;
3. Instance generation plan;
4. cddlib facet analysis plan;
5. Facet clustering;
6. Candidate inequality families;
7. Derivation attempts;
8. Verification status;
9. Family compression status;
10. Proof obligations;
11. Next regulator task.

## Machine-readable artifacts

A completed study iteration should update:

```text
reports/<problem_id>_state.json
reports/<problem_id>_report.md
tasks/TASK_POOL.json
memory/facets/<problem_id>/facet_signatures.json
memory/family/<problem_id>/family_memory.json
```

Family guesses and verifications should be stored under:

```text
memory/family/<problem_id>/guesses/
memory/family/<problem_id>/verifications/
```

## Anti-overfitting rule

Do not introduce a symbolic family solely because it covers one computed facet in one small instance.

A local candidate must remain local unless:

* it appears across multiple instance sizes or regimes;
* it is derived from source constraints;
* it is verified as a specialization of a broader family.

If many local candidates appear, run a family-compression pass.

## Memory rule

Do not clear all memory when starting a new problem.

Use:

```text
memory/facets/<problem_id>/
memory/family/<problem_id>/
memory/facts/<problem_id>/
```

Use global memory only for reusable facts:

```text
memory/facts/global/
```

## Completion rule

The task is incomplete while any of the following remain:

* candidate families without derivation certificates;
* unresolved computed facets without failure chains;
* unverified family guesses;
* invalidated candidates not reflected in revised conditions;
* open high-priority task-pool items;
* missing exact matching checks;
* missing finite validity checks;
* missing derivation certificates for claimed derived families.

Stop only when the regulator state permits stopping or a real blocker is reached.

If blocked, report:

1. completed work;
2. unresolved items;
3. blocker;
4. smallest next action.

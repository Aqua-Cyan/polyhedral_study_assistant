# CLAUDE.md

This repository is a research harness for discovering, testing, and documenting convex-hull descriptions of parametric integer linear sets.

The project is not an automatic theorem prover and not an automatic convex-hull solver. It is a reproducible research workflow that combines:

* problem-specific adapters;
* finite instance generation;
* 0-1 point enumeration;
* cddlib-based convex-hull computation;
* facet normalization and clustering;
* symbolic family guessing;
* finite validity checks;
* derivation certificates;
* regulator-controlled research loops.

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

## Core mathematical rules

Never claim that a candidate inequality system is a complete convex-hull description unless all of the following are true:

1. validity of all inequality families has been proved;
2. completeness has been proved, typically by showing the proposed relaxation is contained in the convex hull;
3. tested cddlib facets are covered, or all exceptions are explicitly reported;
4. all assumptions, parameter ranges, and boundary cases are stated;
5. finite computational evidence is not being mistaken for a symbolic proof.

If only computational evidence is available, label the result as:

* `raw cddlib facet`;
* `candidate`;
* `experimentally supported`;
* `derived for tested scope`;
* `proved valid`;
* `facetness unproved`;
* `complete hull not claimed`.

Do not promote a family from `candidate` to `derived` without a derivation certificate.

Do not promote a family from `derived` to `complete hull` without a completeness proof.

## Repository architecture

The repository is organized around two layers.

### Generic reusable layer

Reusable infrastructure belongs under `src/psa/`.

Examples:

* inequality representation;
* normalization;
* binary point enumeration;
* cdd backend calls;
* exact normalized matching;
* finite validity checking;
* family protocol utilities;
* derivation-attempt records;
* regulator and agent orchestration;
* generic report/state utilities.

Do not put problem-specific mathematics into `src/psa/` unless it is genuinely reusable across multiple problems.

### Problem-specific adapter layer

Problem-specific research models belong under:

```text
examples/<problem_id>/
```

A problem adapter may define:

* variables and canonical ordering;
* feasibility predicate;
* source constraints;
* instance generation;
* problem-specific family templates;
* problem-specific derivation attempts;
* problem-specific report formatting.

A problem adapter should expose a callable study entry point used by the generic driver.

The current standard is:

```python
def run(max_union_size: int = 5) -> dict:
    ...
```

Other problems may interpret the size parameter differently, but the adapter must return a machine-readable state dictionary.

## User problem onboarding

When a user provides a new integer set, they should define it in:

```text
examples/<problem_id>/README.md
```

Do not assume that the generic `scripts/study.py` can parse arbitrary mathematical Markdown into a full study automatically.

Instead:

1. read `examples/<problem_id>/README.md`;
2. create a thin problem-specific adapter under `examples/<problem_id>/`;
3. preserve the user’s original notation in reports;
4. use internal decompositions only as analysis devices;
5. expose a standard `run(...) -> dict` entry point;
6. output state, report, memory, and task-pool artifacts.

## Required artifacts for each study

Every problem-specific study should produce:

```text
reports/<problem_id>_state.json
reports/<problem_id>_report.md
tasks/TASK_POOL.json
memory/facets/<problem_id>/facet_signatures.json
memory/family/<problem_id>/family_memory.json
```

The Markdown report is for humans.

The JSON state and task pool are for the regulator loop.

Do not decide completion from the Markdown report alone. Always inspect the state JSON and task pool.

## Research loop

For integer-hull discovery tasks, follow this loop:

1. formalize the integer set, variables, domains, parameters, and assumptions;
2. create or update the problem adapter;
3. generate staged finite instances;
4. enumerate feasible integer points;
5. compute convex-hull inequalities with cddlib;
6. normalize every inequality;
7. classify bounds, original constraints, nontrivial facets, candidate families, and unresolved records;
8. group facets by support, coefficients, right-hand side, source constraints, and symmetry;
9. propose symbolic family candidates;
10. run exact instantiation matching;
11. run finite validity checks;
12. attempt derivation certificates;
13. update state JSON, memory, task pool, and report;
14. let the regulator decide whether to stop or continue.

Do not stop merely because an intermediate report was produced.

## Goal contract

When the user provides a `\goal ... \endgoal` block, treat it as the stopping contract for the task.

Do not ask whether to continue while the stopping contract is unsatisfied.

A research task is not complete while any of the following remain:

* candidate families without derivation certificates;
* unresolved computed facets;
* facets covered only heuristically;
* invalidated candidates not used to refine conditions;
* computed facets without exact matching status;
* candidate families without finite validity checks;
* unverified family guesses;
* open high-priority research tasks in `tasks/TASK_POOL.json`.

Only stop when the goal condition is satisfied or a real blocker is reached.

If a blocker is reached, report:

1. what was completed;
2. what remains unresolved;
3. why the blocker prevents progress;
4. the smallest next action needed to continue.

## Instance scaling rule

Do not rely only on the smallest examples.

Use a staged instance plan:

1. tiny sanity instances for debugging conventions and feasibility predicates;
2. small structured instances to reveal initial facet patterns;
3. medium structured instances to test generalization;
4. random or exhaustive sweeps within computational limits;
5. targeted edge cases for suspected missing families.

For 0-1 sets, include instances large enough to distinguish:

* singleton supports;
* pair supports;
* proper subset supports;
* full-set supports;
* overlapping supports;
* nested supports;
* asymmetric threshold cases.

If larger instances are too expensive, state the computational bottleneck and generate targeted structured cases rather than stopping at tiny examples.

## Anti-overfitting rule

Do not create many narrowly tailored families merely to cover the current computed facets.

An inequality family is suspiciously over-specialized if it mentions:

* concrete variable names from one instance;
* a fixed tested instance size;
* a fixed support that is not required by the mathematical model;
* a single cddlib facet as its only evidence;
* no source constraints or derivation route.

A family based on one small-instance facet must remain a `local candidate` unless it has a derivation certificate or is clearly a specialization of a more general valid family.

## Family compression rule

Before final reporting, perform a family-compression pass if many candidate families or candidate facets have similar structure.

The compression pass should:

1. group candidate facets by source constraints;
2. group by support pattern;
3. group by coefficient pattern;
4. group by right-hand side pattern;
5. group by parameter regime;
6. ask whether several candidates are special cases of a common parameterized family;
7. propose a smaller number of general symbolic families;
8. instantiate the proposed family on tested instances;
9. check exact normalized matching;
10. check finite validity;
11. seek a derivation certificate;
12. retain narrow families only when no valid generalization is found.

Prefer a small number of parameterized families over a long list of ad hoc inequalities.

## Candidate family validation pipeline

A candidate family must pass these gates before being treated as derived.

### Gate 1: exact instantiation matching

For every claimed covered facet:

1. instantiate the symbolic family on the concrete instance and parameter values;
2. generate the concrete inequality;
3. normalize the instantiated inequality;
4. normalize the computed cddlib facet;
5. check exact equality.

Do not count visual similarity or informal resemblance as coverage.

### Gate 2: finite validity check

Every candidate family instance should be checked on all enumerated feasible integer points for the corresponding tested instance.

If a feasible point violates the instantiated inequality, the family instance must be reported as invalidated.

The invalidation record should include:

* concrete instance;
* family parameter values;
* instantiated inequality;
* violating feasible point;
* violation value if available.

### Gate 3: derivation certificate check

A family may be reported as derived or proved valid only if it has a derivation certificate.

A derivation certificate should record:

* source constraints;
* selected subsets or parameter values;
* intermediate derived rows;
* use of bounds;
* residualization steps;
* coefficient tightening steps;
* MIR, mixed MIR, or MIR-over-MIR steps if used;
* reconstruction of the target inequality;
* symbolic parameter conditions;
* limitations and boundary cases.

## Unmatched facet protocol

A computed nontrivial facet must not be reported as merely unmatched until the assistant has attempted:

1. source-constraint identification by support overlap;
2. residual derivation;
3. coefficient tightening;
4. aggregation plus c-MIR;
5. mixed MIR;
6. MIR-over-MIR or derived-row reuse;
7. family compression against similar facets;
8. symbolic generalization if a concrete derivation is found.

Only if these attempts fail should the facet appear in the unresolved section, with explicit failure reasons.

## Regulator loop

The repository supports a regulator-controlled research loop.

The loop reads:

```text
reports/<problem_id>_state.json
tasks/TASK_POOL.json
memory/facets/<problem_id>/
memory/family/<problem_id>/
```

The regulator decides the next role:

* `FamilyGuesser`;
* `Verifier`;
* `DerivationProver`;
* `StudyAdapter`;
* generic executor.

Do not override the regulator’s decision without a reason.

If the regulator chooses a specific task, complete that task rather than switching to unrelated work.

## Agent roles

### FamilyGuesser

The FamilyGuesser proposes general symbolic families from clustered candidate facets.

It should:

* inspect candidate facet clusters;
* avoid over-specialized local families;
* propose subset-parameterized forms;
* identify expected source constraints;
* identify expected derivation routes;
* write guesses under `memory/family/<problem_id>/guesses/`.

It must not mark a family as derived or proved.

### Verifier

The Verifier checks family guesses before they are implemented or promoted.

It should:

* inspect the guess JSON;
* check whether the statement is symbolic and well-formed;
* check parameter conditions;
* check whether the guess is over-specialized;
* check whether evidence facets plausibly match the template;
* check whether exact matching is implementable;
* check whether finite validity checking is implementable;
* check whether the derivation route is plausible;
* write verification reports under `memory/family/<problem_id>/verifications/`.

It must not make a weak candidate look stronger than it is.

### DerivationProver

The DerivationProver attempts to derive a candidate family or facet.

It should:

* start from source constraints;
* use residualization, coefficient tightening, aggregation, c-MIR, mixed MIR, or MIR-over-MIR;
* produce a derivation certificate;
* update the problem adapter only when the family passes the appropriate gates.

### StudyAdapter

The StudyAdapter runs the problem-specific computational study.

It should:

* generate instances;
* enumerate feasible points;
* compute hull inequalities;
* classify and normalize facets;
* update state/report/memory/task artifacts.

## Memory organization

Do not clear the entire `memory/` directory when starting a new problem.

Use problem-specific memory:

```text
memory/facets/<problem_id>/
memory/family/<problem_id>/
memory/facts/<problem_id>/
```

Use global memory only for reusable mathematical or workflow facts:

```text
memory/facts/global/
```

Examples of global facts:

* residual inequality pattern;
* coefficient tightening template;
* mixed MIR template;
* exact matching gate;
* finite validity gate;
* reporting standards.

## Reporting standard

The main report must be family-first, not instance-first.

Instance-level data may appear in:

* compact evidence tables;
* coverage tables;
* appendices;
* machine-readable state JSON.

For each reported family, include:

1. symbolic statement in the original notation;
2. parameter conditions;
3. source constraints;
4. derivation certificate or derivation status;
5. examples of concrete facets covered;
6. exact matching status;
7. finite validity status;
8. facetness status;
9. completeness status;
10. unresolved proof obligations.

Do not present raw cddlib facets as the final result.

## Code-change rules

Prefer small, reviewable changes.

When modifying code:

1. keep generic utilities in `src/psa/`;
2. keep problem-specific logic in `examples/<problem_id>/`;
3. add or update tests when changing behavior;
4. rerun relevant tests or study scripts;
5. avoid large rewrites unless necessary;
6. preserve machine-readable state outputs;
7. do not silently change status labels to stronger claims.

## Expected final response after a task

At the end of each task, report:

1. files changed;
2. tests or study commands run;
3. whether candidate, unresolved, or unverified counts changed;
4. which task id was completed or remains open;
5. what should happen next;
6. any blocker or uncertainty.

# CLAUDE.md

This repository is a research harness for discovering and validating convex hull descriptions of integer linear sets.

## Project role

Act as a careful mathematical programming research assistant and software engineer.

Do not treat this project as an automatic convex hull solver. The goal is to support a reproducible research workflow for discovering, testing, deriving, and documenting convex-hull inequality families.

The central method is:

1. compute small-instance facets;
2. understand each nontrivial facet through source constraints and c-MIR-style derivations;
3. generalize concrete derivations into symbolic inequality families;
4. validate the proposed families computationally and mathematically;
5. repeat until every computed facet is either derived, invalidated as a candidate, or explicitly unresolved with a documented failed derivation path.

## Core rules

Never claim that a candidate inequality system is a complete convex hull description unless:

1. validity of all inequality families has been proved;
2. completeness has been proved, typically by showing the candidate polyhedron is contained in the convex hull;
3. tested cddlib facets are covered or all exceptions are explicitly reported;
4. all assumptions, parameter ranges, and boundary cases are stated.

If only computational evidence is available, label the result as `experimentally supported` or `conjectural`.

Problem-specific research models should usually live under `examples/<name>/` or `studies/<name>/`, not directly under `src/psa/`, unless they are intended to become reusable built-in benchmarks.

Do not silently discard equations returned by a polyhedral backend. If equations are present and the backend or report does not support them, state this limitation explicitly.

## Non-stopping rule

Do not stop after one pass through the facets.

A run is incomplete if any nontrivial computed facet is:

* not exactly matched by a symbolic family;
* matched only heuristically;
* valid on tested points but lacking a derivation certificate;
* invalidated but not used to refine the candidate conditions;
* unresolved without documented c-MIR pattern attempts.

If the convex hull is not completely proved, continue the discovery loop until one of the following is true:

1. every computed nontrivial facet is covered by a derived/proved family;
2. every remaining facet has a documented failed derivation attempt for each relevant pattern;
3. the user explicitly asks to stop;
4. a computational or mathematical blocker is identified and reported.

Do not end the analysis merely because some candidate families were found.

## Research workflow

For integer hull discovery tasks, follow this sequence:

1. Formalize the integer set, variables, parameters, and relaxation.
2. Generate small test instances, including edge cases and random cases.
3. Enumerate integer points and compute facets by cddlib.
4. Normalize all inequalities.
5. Classify facets by support, coefficient pattern, symmetry, and source-constraint overlap.
6. For every nontrivial facet, identify possible source constraints.
7. Try to derive the concrete facet using documented c-MIR patterns.
8. Once a concrete derivation is found, generalize the same derivation to a symbolic family.
9. Instantiate the symbolic family on all tested instances.
10. Check exact matching against computed cddlib facets.
11. Check finite validity on all enumerated feasible points.
12. If invalid, output counterexamples and refine the candidate.
13. If valid on tested points but lacking a derivation, keep it as a candidate and continue attempting c-MIR derivations.
14. If a derivation certificate exists, move the family to derived/proved status.
15. Repeat the loop until all computed facets are classified.

Computed facets are not the final output. For a parametric integer set, the final research output should be symbolic inequality families with derivations. A report that only lists instance-level facets is incomplete.

## Facet-first derivation rule

For every nontrivial computed facet, use this order:

1. Rewrite the concrete facet in the original model notation.
2. Identify which original constraints contain the variables in the facet support.
3. Identify which variable bounds or complements may be needed.
4. Try to derive the concrete facet from those source constraints using the documented c-MIR patterns.
5. If a derivation succeeds for the concrete facet, generalize the derivation symbolically.
6. Only then propose the symbolic family as a derived family.
7. If no derivation is found, keep the family as candidate or unresolved, not proved.

Do not begin by guessing a broad symbolic inequality and fitting facets to it. Broad symbolic guesses are allowed, but they must be validated and either derived, refined, or invalidated.

## Required c-MIR pattern attempts

For each unmatched or nontrivial facet, try the following patterns before reporting it as unresolved.

### Pattern 1: residual inequality

Use when a facet resembles

[
x(D)\ge \alpha y.
]

From a source row

[
x(J)\ge by
]

and binary upper bounds on (J\setminus D), derive

[
x(D)\ge (b-|J\setminus D|)y
]

when (b-|J\setminus D|>0).

Do not restrict this pattern only to the minimal cover case (|D|=|J|-b+1). The general residual family must be considered:

[
x(D)\ge (b-|J\setminus D|)y,\quad D\subseteq J,\quad b-|J\setminus D|>0.
]

### Pattern 2: coefficient tightening

Use when a direct combination of source constraints gives coefficients that are too weak or has extra variables.

Try:

* upper-bound substitution;
* lower-bound substitution;
* complementing binary variables;
* tightening coefficients on activation variables;
* eliminating variables outside the target support.

Document the pre-tightening inequality and the tightened inequality.

### Pattern 3: aggregation plus c-MIR

Use when the target facet appears to involve multiple original constraints.

Try nonnegative aggregation of original constraints, then apply c-MIR or c-MIR-style residualization. Record:

* aggregation multipliers;
* aggregated inequality;
* integer part;
* continuous or bounded part;
* rounding step;
* final inequality.

### Pattern 4: mixed MIR

Use only when base inequalities can be written in a valid mixed-MIR form. Record:

* base inequalities;
* (f^i(x)), (g^i(x)), (B), and (\pi_i);
* proof that (f^i(x)\ge 0);
* proof that (g^i(x)) is integral;
* (\tau_i) and (\gamma_i);
* ordering by (\gamma_i);
* common dominating function (\bar f);
* unsimplified mixed-MIR inequality;
* simplification to the target inequality.

Do not call ordinary addition of constraints “mixing.”

### Pattern 5: MIR after MIR

A derived valid inequality may become a new source row.

After deriving a residual, coefficient-tightened, or mixed-MIR inequality, try applying another c-MIR pattern to it together with other source rows. This is allowed and should be documented as a multi-step derivation.

Example route:

[
\text{original row}
\to
\text{residual row}
\to
\text{mixed MIR with another residual row}
\to
\text{coefficient tightening}
\to
\text{target facet}.
]

## Candidate family validation pipeline

When studying a parametric integer set, computed facets are evidence, not final mathematical output.

Use this pipeline:

```text
computed cdd facets
  ↓
facet normalization
  ↓
source-constraint identification
  ↓
concrete c-MIR derivation attempts
  ↓
candidate family proposal
  ↓
Gate 1: instantiation matching
  ↓
Gate 2: finite validity check
  ↓
Gate 3: derivation certificate check
  ↓
family-first report
  ↓
refinement loop if unresolved or invalidated candidates remain
```

### Gate 1: instantiation matching

A symbolic family may not claim to cover a computed facet unless the following check is performed:

1. instantiate the symbolic family on the concrete test instance and chosen family parameters;
2. generate the concrete `LinearInequality`;
3. normalize the instantiated inequality;
4. normalize the computed cddlib facet;
5. check exact equality.

Do not count a facet as covered by visual similarity or informal pattern resemblance.

If exact normalized equality fails, the facet is not covered by that family.

### Gate 2: finite validity check

Every candidate family instance must be checked on all enumerated feasible 0-1 points of the corresponding small instance.

If a feasible point violates the instantiated inequality, the family instance must be placed in `Invalidated candidate families`.

The report must include:

* concrete instance;
* family parameter values;
* instantiated inequality;
* violating feasible point;
* violation value if available.

An invalidated family must not appear as a derived or proved family.

### Gate 3: derivation certificate check

A candidate family may be reported as derived or proved valid only if it has a derivation certificate using documented patterns, such as:

* residual inequality;
* coefficient tightening;
* aggregation;
* c-MIR;
* mixed MIR;
* sequential MIR or MIR applied after MIR.

The certificate must record:

* source constraints;
* substitutions or bounds used;
* intermediate inequalities;
* rounding, MIR, or mixing step if used;
* final symbolic inequality;
* equality check between reconstructed inequality and the computed facet when claiming coverage.

A family that passes finite tests but lacks a derivation certificate must be labeled as `candidate`, not `proved valid`.

## Candidate refinement loop

For every proposed candidate family:

1. instantiate it on all tested small instances;
2. check exact matching against cdd facets;
3. check finite validity on all enumerated feasible 0-1 points;
4. if invalid, produce a counterexample;
5. use the counterexample to refine the parameter conditions;
6. if valid on tests but no derivation exists, keep it in `Candidate symbolic inequality families`;
7. try to derive it using the documented c-MIR patterns;
8. only after a derivation certificate exists may it move to `Derived or proved symbolic inequality families`;
9. rerun the report after each refinement.

Do not stop immediately after invalidating a candidate. Invalidated candidates are useful: they show which conditions are missing. 

A failed direct derivation is not a failed derivation. The assistant must try derived-row reuse: first derive intermediate valid inequalities, then use them as new source rows for further residual, tightening, c-MIR, mixed-MIR, or MIR-after-MIR attempts.

## No unsupported residual summation

Do not add two residual demands and claim the result is valid unless the derivation explicitly handles overlap and overcounting.

If two residual demands use the same (x)-support, the assistant must:

1. check finite validity on enumerated feasible points;
2. identify whether the same (x)-variables are being counted twice;
3. provide a c-MIR, coefficient-tightening, mixed-MIR, or other valid derivation certificate;
4. otherwise keep the formula as a candidate or invalidated family.

Computed coverage does not imply validity.

Finite validity does not imply general proof.

A derivation certificate is required for a proved-valid claim.

## Reporting rules

The report must be family-first.

Use the following sections:

1. model and assumptions;
2. tested instances and computational scope;
3. derived/proved symbolic families;
4. candidate symbolic families;
5. invalidated candidate families with counterexamples;
6. exact coverage table;
7. derivation attempts for not-yet-covered facets;
8. unresolved computed facets;
9. proof obligations;
10. next loop instructions.

Do not place raw instance-level facets in the main body unless the user asks for raw computational output. Put raw facets in an appendix or a machine-readable artifact.

## Coding rules

Use Python for the initial harness.

Prefer small, testable modules.

Every nontrivial mathematical transformation should have a unit test.

Do not hard-code results unless they are explicitly stored as test fixtures or example data.

For each new inequality family or derivation pattern, add tests that check:

1. the symbolic family instantiates to the expected concrete inequality;
2. the instantiated inequality is valid on enumerated feasible points;
3. exact matching against cdd facets works when expected;
4. invalid candidates produce counterexamples;
5. derivation certificates reconstruct the final inequality.

## Initial modules

The first implementation should focus on:

* `inequality.py`: representation of linear inequalities;
* `normalize.py`: gcd reduction, sign normalization, support extraction;
* `report.py`: family-first Markdown reports;
* `validity.py`: finite feasible-point validity checks;
* `family.py`: candidate family instantiation and matching;
* tests for normalization, validity, family instantiation, and derivation certificates.

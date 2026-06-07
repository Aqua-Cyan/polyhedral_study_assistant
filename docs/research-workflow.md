# Research Workflow for Integer Hull Discovery

This document defines the required workflow for discovering symbolic convex-hull inequality families from small computed integer hulls.

The workflow is not:

```text
compute facets -> list facets -> stop
```

The workflow is:

```text
compute facets
-> identify source constraints
-> derive concrete facets using c-MIR patterns
-> generalize derivations
-> validate symbolic families
-> refine candidates
-> repeat until all computed facets are classified
```

## 1. Formalize the model

For every problem, record:

* integer set (S);
* continuous relaxation (P);
* variable domains;
* parameter assumptions;
* index-set assumptions;
* target object, such as (\operatorname{conv}(S)), a valid inequality family, a facet family, or an extended formulation.

For set systems involving subsets (J_1,J_2,\ldots), explicitly state whether these sets may overlap, be nested, be disjoint, or be identical.

If useful, introduce internal decompositions such as:

[
J_1\setminus J_2,\qquad
J_2\setminus J_1,\qquad
J_1\cap J_2.
]

These decompositions are analysis devices. The final mathematical statements should also be expressible in the user's original notation.

## 2. Generate small instances

Generate small instances that expose different structures:

* disjoint index sets;
* overlapping index sets;
* nested index sets;
* identical index sets;
* small right-hand sides;
* tight right-hand sides;
* boundary cases such as (b=1) and (b=|J|);
* asymmetric parameter cases;
* random cases.

The purpose of small instances is not to prove the hull. The purpose is to reveal concrete facets that can be explained and generalized.

## 3. Compute integer hull facets

For each small instance:

1. enumerate feasible integer points or use the configured integer-point backend;
2. compute the convex hull with cddlib or another polyhedral backend;
3. normalize all inequalities;
4. separate bounds, original constraints, and nontrivial facets;
5. record support, coefficient pattern, right-hand side, and symmetry class.

If the backend returns equations, record them. Do not silently discard equations.

## 4. Facet-to-family discovery rule

Do not stop after listing instance-level facets.

For every nontrivial facet found in a small instance:

1. translate the concrete inequality into the original symbolic notation;
2. identify which original constraint or constraints contribute variables to the facet;
3. identify which variable bounds are implicitly used;
4. try to derive the concrete inequality from those source constraints using c-MIR, aggregation, complementation, coefficient tightening, upper-bound substitution, mixed MIR, or MIR-after-MIR;
5. after a concrete derivation is found, generalize the same derivation to the original parametric model;
6. state the resulting symbolic inequality family;
7. instantiate the family back on the tested examples;
8. verify exact matching against computed facets;
9. verify finite validity on enumerated feasible points;
10. only then include the family as derived/proved in the report.

A family without a derivation certificate may be reported only as a candidate.

A family with a violating feasible point must be reported as invalidated.

## 5. Required c-MIR derivation patterns

For each nontrivial facet, try the following patterns before declaring it unresolved.

### 5.1 Residual pattern

Given a source row

[
x(J)\ge by,
]

and (D\subseteq J), let (E=J\setminus D). Since (x(E)\le |E|),

[
x(D)+x(E)\ge by
]

implies

[
x(D)\ge (b-|E|)y
]

whenever (b-|E|>0).

This is the general residual family:

[
x(D)\ge (b-|J\setminus D|)y,
\qquad D\subseteq J,
\qquad b-|J\setminus D|>0.
]

Do not restrict this pattern to (|D|=|J|-b+1). That special case gives coefficient (1), but larger residual coefficients may also be important.

### 5.2 Coefficient tightening pattern

Use coefficient tightening when a direct source row or aggregate has extra variables or coefficients that are too weak.

Record:

* source constraints;
* target support;
* variables eliminated;
* bounds used;
* pre-tightening inequality;
* tightened coefficients;
* final inequality.

Allowed operations include:

* upper-bound substitution (x_j\le 1);
* lower-bound substitution (x_j\ge 0);
* binary complementation;
* support restriction;
* coefficient strengthening on binary activation variables;
* tightening after aggregation;
* tightening after MIR.

### 5.3 Aggregation plus c-MIR

Use this pattern when the facet appears to use multiple original constraints.

Record:

* source constraints;
* nonnegative multipliers;
* aggregated inequality;
* integer variables;
* continuous or bounded part;
* MIR or c-MIR rounding step;
* final inequality.

Do not claim that an aggregate gives the target facet unless every eliminated variable and every coefficient change is justified.

### 5.4 Mixed MIR pattern

Use mixed MIR only when the base inequalities can be put in a documented mixed-MIR form.

For each base inequality, record:

[
f^i(x)+B g^i(x)\ge \pi_i.
]

Also record:

* (f^i(x)\ge 0);
* (g^i(x)\in\mathbb Z);
* common (B), or a justified scaling to obtain a common (B);
* (\tau_i=\lceil \pi_i/B\rceil);
* (\gamma_i=\pi_i-(\tau_i-1)B);
* ordering by (\gamma_i);
* common dominating function (\bar f);
* unsimplified mixed-MIR inequality;
* final simplification.

Ordinary addition of constraints is not mixed MIR.

### 5.5 MIR after MIR

A derived inequality can become a new source row.

After obtaining a residual, coefficient-tightened, or mixed-MIR inequality, try applying another MIR-type pattern to it with additional source constraints.

Examples:

```text
original row -> residual row -> mixed MIR -> coefficient tightening
original row -> coefficient tightening -> MIR
original row -> residual row -> aggregation with another residual row -> c-MIR
```

Every stage must be recorded.

## 6. Unmatched facet derivation protocol

A computed facet must not be reported as merely `unmatched` until the assistant has attempted:

1. source-constraint identification by support overlap;
2. residual derivation from each relevant source row;
3. coefficient tightening;
4. aggregation of multiple original or derived rows;
5. c-MIR or mixed-integer rounding;
6. mixed MIR if valid base inequalities can be formed;
7. MIR after MIR;
8. candidate-family proposal and finite validation;
9. symbolic generalization if any concrete derivation succeeds.

Only if all attempts fail may the facet be placed in the unresolved section, and the report must state which attempts failed.

## 7. Candidate family validation gate

Every candidate family must pass these gates before it can be promoted to a derived/proved family.

### Gate 1: exact instantiation matching

A symbolic family covers a computed facet only if:

1. the family is instantiated with explicit parameter values;
2. the instantiated inequality is normalized;
3. the computed cddlib facet is normalized;
4. the two normalized inequalities are exactly equal.

Visual similarity is not enough.

### Gate 2: finite validity check

Every candidate family instance must be checked against all enumerated feasible integer points in the tested instance.

If a feasible point violates the inequality, report:

* instance;
* family parameter values;
* instantiated inequality;
* violating point;
* violation value.

The family must be labeled invalidated or refined.

### Gate 3: derivation certificate check

A family can be labeled `derived` or `proved valid` only if it has a derivation certificate.

The certificate must include:

* source constraints;
* intermediate inequalities;
* bounds and substitutions;
* MIR, c-MIR, mixing, or tightening step;
* final symbolic inequality;
* parameter conditions;
* exact matching evidence when claiming coverage.

If a family passes finite tests but lacks this certificate, it remains a candidate.

## 8. Candidate refinement loop

The workflow is iterative.

For each candidate family:

1. instantiate it on all tested instances;
2. check exact matching against cdd facets;
3. check finite validity;
4. if invalid, produce counterexamples;
5. use counterexamples to refine the candidate conditions;
6. if valid but underived, attempt derivations using all relevant c-MIR patterns;
7. if a derivation is found, promote to derived/proved family;
8. rerun the facet coverage report.

Do not stop at the first candidate.

Do not stop after invalidating a candidate.

Do not stop while unexplained computed facets remain unless the user asks to stop or a blocker is clearly reported.

## 9. Reporting standard

Reports must be organized by symbolic inequality family, not by computational instance.

Use these sections:

1. model and assumptions;
2. computational scope;
3. derived/proved symbolic families;
4. candidate symbolic families;
5. invalidated candidate families with counterexamples;
6. coverage of computed facets;
7. derivation attempts for not-yet-covered facets;
8. unresolved computed facets;
9. proof obligations;
10. next refinement loop.

Instance-level data belongs only in:

* compact evidence tables;
* coverage tables;
* appendices;
* machine-readable JSON artifacts.

## 10. Proof status labels

Use these labels carefully:

* `raw cddlib facet`;
* `normalized`;
* `variable bound`;
* `original constraint`;
* `derived for concrete instance`;
* `derived symbolic family`;
* `proved valid`;
* `candidate`;
* `experimentally supported`;
* `invalidated`;
* `unresolved`;
* `facetness unproved`;
* `complete hull not claimed`;
* `complete hull proved`.

Do not confuse these statuses:

* exact matching is not validity;
* finite validity is not proof;
* validity is not facetness;
* facet coverage is not completeness;
* a complete hull requires reverse inclusion.

## 11. Completion criteria for one research run

A research run may stop only when one of the following holds:

1. every computed nontrivial facet is covered by a derived/proved family;
2. every remaining facet is unresolved with documented failed derivation attempts;
3. all candidate families are either promoted, invalidated, or explicitly left as candidates with next actions;
4. a blocker is reported;
5. the user asks to stop.

If none of these holds, continue the loop.

## Instance scaling plan

Small instances are used to discover patterns, but tiny instances can cause overfitting.

Every study should use a staged instance plan.

### Stage 1: sanity instances

Use the smallest cases only to test:

- variable ordering;
- feasibility enumeration;
- cddlib backend;
- normalization;
- report generation.

Do not infer final symbolic families from this stage alone.

### Stage 2: structured small instances

Generate instances that isolate structural cases:

- disjoint sets;
- one-element overlap;
- larger overlap;
- nested sets;
- identical sets;
- boundary thresholds;
- asymmetric thresholds.

### Stage 3: medium generalization instances

Increase sizes enough to distinguish different support patterns.

For 0-1 problems, this means including cases where possible supports include:

- singleton subsets;
- pairs;
- triples;
- proper subsets;
- full support.

For two-set models, include cases where each of the regions

\[
J_1\setminus J_2,\quad J_1\cap J_2,\quad J_2\setminus J_1
\]

can have size 0, 1, and at least 2 when feasible.

### Stage 4: random or exhaustive sweep

Within computational limits, run either:

- exhaustive sweeps over small-to-medium parameters; or
- random sampled instances with fixed seed.

Use this stage to test proposed families, find counterexamples, and discover missing facets.

### Rule

A symbolic family supported only by tiny cases must be labeled as a local candidate. It should not be promoted unless it passes derivation and validation gates.

## Family compression pass

After candidate families are generated, run a family-compression pass before final reporting.

The goal is to avoid a long list of ad hoc inequalities that only fit the tested examples.

### Compression procedure

1. Collect all candidate and derived families.
2. Group them by:
   - source constraints;
   - support pattern;
   - coefficient pattern;
   - right-hand side pattern;
   - derivation route;
   - parameter regime.
3. Ask whether several families are special cases of a broader family.
4. Propose a general symbolic family using arbitrary subsets and parameter expressions.
5. Instantiate the general family on all tested instances.
6. Check exact matching against computed facets.
7. Check finite validity on enumerated feasible points.
8. Attempt a c-MIR derivation certificate.
9. If successful, replace narrow families with the general family and list narrow cases as examples.
10. If unsuccessful, keep the narrow families but record why generalization failed.

### Warning signs of over-specialization

A family is probably too narrow if:

- it mentions fixed variable names;
- it mentions a concrete tested instance size;
- it only covers one facet;
- it differs from another family only by replacing one subset with another;
- it has no source-constraint explanation;
- it cannot be expressed using original model notation.

### Preferred report style

Prefer:

\[
x(D)\ge (b-|J\setminus D|)y,\quad D\subseteq J
\]

over separate families such as:

\[
x_i\ge y,\quad x_i+x_j\ge y,\quad x_i+x_j+x_k\ge 2y.
\]

The latter should appear as special cases, not as separate unrelated families, whenever a common derivation exists.

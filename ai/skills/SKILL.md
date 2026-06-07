---

name: integer-hull-discovery
description: use this skill when analyzing integer linear sets, discovering convex hull descriptions, interpreting cddlib-generated facets, deriving valid inequalities with c-MIR, validating candidate facet families, or tracking proof obligations for integer hull descriptions.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Integer Hull Discovery

When asked to analyze the convex hull of an integer linear set, do not guess the final convex hull description directly.

Use a staged and iterative research workflow. Treat computational evidence, valid inequality derivations, facetness proofs, and complete hull proofs as different levels of evidence.

The central goal is not to list computed facets. The goal is to derive symbolic inequality families from concrete computed facets.

## Required workflow

1. Formalize the set.

   * Define all variables, domains, index sets, parameters, and assumptions.
   * State whether index sets may overlap.
   * State whether parameters satisfy feasibility assumptions.
   * Preserve the user's notation.
   * If useful, internally analyze intersections, differences, nested cases, and symmetry classes.

2. Identify the intended goal.

   * Complete convex hull description.
   * Valid inequality family.
   * Facet family.
   * Separation routine.
   * Extended formulation.
   * Computational exploration only.

3. Generate or request small instances.

   * Include boundary cases.
   * Include overlapping and non-overlapping index-set cases when relevant.
   * Include cases where parameters are tight, such as (b=1) or (b=|J|).
   * Include random cases if possible.

4. Compute and normalize facets.

   * Enumerate feasible integer points for small instances.
   * Use cddlib or the configured backend to compute hull facets.
   * Normalize every inequality.
   * Record support, coefficient pattern, right-hand side, and symmetry class.
   * Distinguish variable bounds, original constraints, and nontrivial facets.

5. For every nontrivial facet, identify source constraints.

   * Rewrite the concrete facet in the user's original notation.
   * Identify which original constraints contain the variables in the facet support.
   * Identify which variable bounds, complements, or derived rows may be useful.

6. Derive the concrete facet before generalizing.

   * Try residual inequalities.
   * Try coefficient tightening.
   * Try aggregation plus c-MIR.
   * Try mixed MIR when valid base inequalities can be formed.
   * Try MIR after MIR, using already derived valid inequalities as new source rows.
   * Record the derivation as a certificate, not only as prose.

7. Generalize only after concrete derivation.

   * Turn a successful concrete derivation into a symbolic family.
   * State all index conditions and parameter ranges.
   * Specify whether the family is proved valid, candidate, invalidated, facet-defining, or complete.

8. Validate candidate families.

   * Instantiate the family on tested small instances.
   * Check exact normalized equality against computed facets when claiming coverage.
   * Check finite validity on all enumerated feasible integer points.
   * If invalid, produce a counterexample.
   * If finite-valid but underived, keep it as candidate and continue trying c-MIR patterns.
   * If a derivation certificate exists, promote it to derived/proved valid.

9. Repeat.

   * Do not stop after one report if facets remain unexplained.
   * Do not stop after finding one candidate family.
   * Do not stop after invalidating one candidate family.
   * Refine candidates and rerun validation until all computed facets are classified or a blocker is reported.

10. Prove or label honestly.

* Never call a description "the convex hull" unless completeness is proved.
* If only small examples support it, label it `experimentally supported`.
* If finite tests pass but no derivation exists, label it `candidate`.
* If a feasible point violates it, label it `invalidated`.
* If validity is proved but completeness is not, say so explicitly.

## c-MIR pattern priority

For every unfamiliar computed facet, use the following derivation order before reporting it as unresolved.

### Residual pattern

Given

[
x(J)\ge by
]

and (D\subseteq J), use (x(J\setminus D)\le |J\setminus D|) to derive

[
x(D)\ge (b-|J\setminus D|)y
]

when (b-|J\setminus D|>0).

Do not restrict this to the minimal case where the coefficient is (1). Larger residual coefficients must also be considered.

### Coefficient tightening

If an aggregate or source row contains extra variables or weak coefficients, try:

* upper-bound substitution;
* lower-bound substitution;
* binary complementation;
* eliminating variables outside target support;
* tightening coefficients on activation variables;
* tightening after residualization;
* tightening after MIR.

Record the pre-tightening and post-tightening inequalities.

### Aggregation plus c-MIR

If the facet involves multiple source constraints, try nonnegative aggregation and then c-MIR.

Record:

* multipliers;
* aggregate row;
* integer variables;
* bounded variables;
* rounding step;
* final inequality.

### Mixed MIR

Use mixed MIR only when the base inequalities are put into a valid mixed-MIR form. Record:

* (f^i(x)+B g^i(x)\ge \pi_i);
* (f^i(x)\ge0);
* (g^i(x)\in\mathbb Z);
* (B,\pi_i,\tau_i,\gamma_i);
* ordering by (\gamma_i);
* common (\bar f);
* unsimplified mixed-MIR formula;
* simplified final inequality.

Do not call ordinary addition of constraints "mixing."

### MIR after MIR

A derived valid inequality may become a new source row.

It is allowed to apply MIR after residualization, after coefficient tightening, or after a previous MIR. Document each stage.

## Candidate family validation gate

Do not move directly from computed facets to a claimed symbolic family.

Use this pipeline:

```text
computed facets
→ normalize facets
→ identify source constraints
→ try concrete c-MIR derivations
→ propose candidate symbolic family
→ instantiate family on concrete test instances
→ check exact matching against computed facets
→ check finite validity on enumerated feasible integer points
→ require a derivation certificate
→ write family-first report
→ repeat if unresolved facets or candidates remain
```

## Exact matching requirement

A computed facet is covered by a symbolic family only if:

1. the family is instantiated with explicit parameter values;
2. the instantiated inequality is normalized;
3. the computed facet is normalized;
4. the two normalized inequalities are exactly equal.

Do not report coverage based only on visual similarity or coefficient resemblance.

## Finite validity requirement

Every candidate family instance must be checked against all enumerated feasible integer points in the tested small instance.

If a violating point is found, report the candidate as invalidated and include:

* tested instance;
* family parameter values;
* instantiated inequality;
* violating point;
* violation value or violated side.

Invalidated candidates must not appear as proved or derived families.

## Derivation certificate requirement

A family can be labeled `proved valid` or `derived` only if it has a derivation certificate.

The certificate must use one or more documented derivation patterns:

* residual inequality;
* coefficient tightening;
* aggregation;
* c-MIR;
* mixed MIR;
* sequential MIR or MIR applied after MIR.

The certificate must include:

* source constraints;
* intermediate inequalities;
* bound substitutions;
* rounding or mixing step when used;
* final symbolic inequality;
* parameter conditions;
* equality check against computed facets when claiming coverage.

## Candidate status rule

Use these statuses carefully:

* `derived/proved valid`: exact matching, finite validity, and derivation certificate are all available.
* `candidate`: finite tests may support the family, but a derivation certificate is missing.
* `invalidated`: a tested feasible point violates an instantiated inequality.
* `unresolved`: no valid family or derivation attempt currently explains the facet.

A family that passes finite tests but lacks a derivation certificate must remain a candidate.

A family that fails finite validity must be reported as invalidated with a counterexample.

## No unsupported summation of residual demands

Do not add residual inequalities from multiple source constraints and claim the result is valid by default.

Before reporting such a formula as valid, explicitly address:

* whether the same (x)-variables are being counted multiple times;
* whether overlap creates overcounting;
* whether c-MIR, mixed MIR, coefficient tightening, or another valid transformation justifies the result;
* whether finite feasible-point checks support the instantiated inequality.

If these checks fail, downgrade the formula to candidate or invalidated status.

## Do not stop at unmatched facets

When a computed facet is not covered by an existing symbolic family, do not immediately report it as unmatched.

First perform a derivation attempt:

1. identify source constraints whose supports overlap the target facet;
2. try residualization from each relevant source row;
3. try nonnegative aggregation and coefficient tightening;
4. try c-MIR or c-MIR-style residualization;
5. try mixed MIR if the base rows can be put into the required form;
6. try MIR after MIR using previously derived inequalities;
7. if the target facet is derived for the concrete instance, generalize the same derivation symbolically;
8. only after these attempts fail may the facet be reported as unresolved.

The report must include the derivation attempt, not just the unresolved inequality.

## Required output sections

Use these sections unless the user requests a different format:

1. Problem formalization
2. Assumptions and edge cases
3. Small-instance plan
4. Computed facet summary
5. Derived/proved symbolic inequality families
6. Candidate symbolic inequality families
7. Invalidated candidate families with counterexamples
8. c-MIR derivation attempts
9. Exact coverage table
10. Unresolved facets
11. Proof obligations
12. Next refinement loop

## Report organization rule

Organize research reports by inequality family, not by computational instance.

Instance-level output belongs only in a compact evidence table or appendix. Do not list all variable bounds or all concrete inequalities in the main body unless the user explicitly asks for raw computational output.

## Hard rule

Never claim that a system of inequalities gives the convex hull unless both inclusions are proved:

1. every integer feasible point satisfies the proposed inequalities;
2. every point satisfying the proposed inequalities belongs to the convex hull.

If the reverse inclusion is missing, state the missing proof obligation explicitly.

## Completion rule

A research run is not complete while any computed nontrivial facet remains unexplained.

Continue the refinement loop unless:

1. all computed nontrivial facets are covered by derived/proved families;
2. all remaining facets have documented failed derivation attempts;
3. all candidate families are either promoted, invalidated, or explicitly left as candidates with next actions;
4. a blocker is reported;
5. the user asks to stop.

## Problem-specific adapter generation

When the user provides a new problem definition under `examples/<problem>/README.md`, do not assume the generic harness already knows the model semantics. Create a thin problem-specific adapter layer under `examples/<problem>/` when needed.

Recommended structure:

```text
examples/<problem>/
  README.md
  model.py
  families.py
  derive.py
  study.py

Allowed responsibilities:

model.py: parse or represent concrete instances, define variable order, feasibility predicate, source constraints, and translation back to the user's notation.
families.py: define problem-specific symbolic or candidate inequality families that implement parameter enumeration and instantiation.
derive.py: identify source constraints for a computed facet and call the generic c-MIR attemptor. It may add problem-specific derivation attempts, but must not label heuristic matches as proved.
study.py: orchestrate instance generation, cdd facet computation, family validation gates, derivation attempts, and report generation.

Forbidden responsibilities:

Do not reimplement cdd backend calls if psa.backends.cdd already provides them.
Do not reimplement inequality normalization.
Do not reimplement finite validity checking.
Do not reimplement exact matching.
Do not reimplement report rendering.
Do not move problem-specific logic into src/psa/ unless it is genuinely reusable across models.

A problem-specific adapter is a bridge between the mathematical model and the generic harness. It is not a second harness.

Every adapter must use the generic pipeline:

computed facets -> source-constraint identification -> generic c-MIR attempts -> problem-specific attempts if needed -> family proposal -> instantiation matching -> finite validity check -> derivation certificate check -> family-first report
```

## MIR-over-MIR rule

When direct derivation from original constraints fails, do not stop.

A valid inequality derived in an earlier step may be used as a new source row in a later step. This includes residual inequalities, coefficient-tightened inequalities, aggregation+c-MIR inequalities, and mixed-MIR inequalities.

For every unresolved facet, try small-depth derivation chains such as:

```text
original row
→ residual row
→ relaxed residual row
→ mixed MIR or aggregation+c-MIR
→ coefficient tightening
→ target facet
```

The assistant must document each intermediate row and its validity reason.

The generic c-MIR attemptor is only a scaffold. If it returns `needs_problem_specific_derivation`, continue with mathematical reasoning using the documented c-MIR patterns. Do not treat a failed generic attempt as proof that the facet cannot be derived. A failed direct derivation is not a failed derivation. The assistant must try derived-row reuse: first derive intermediate valid inequalities, then use them as new source rows for further residual, tightening, c-MIR, mixed-MIR, or MIR-after-MIR attempts.

### Instance scaling requirement

Do not rely only on tiny examples.

Use a staged instance plan:

1. tiny instances for debugging;
2. small structured instances for first pattern discovery;
3. medium structured instances for generalization testing;
4. random or exhaustive sweeps within feasible enumeration limits.

For 0-1 sets, choose instances large enough to distinguish singleton, pair, proper-subset, and full-support inequalities.

For two-set models, include disjoint, overlap, nested, and identical cases. When feasible, include \(|J_1\cup J_2|\ge 4\), \(|J_1\cup J_2|\ge 5\), and asymmetric threshold cases.

If computation becomes expensive, report the bottleneck and switch to targeted structured cases rather than only using tiny examples.

## Family generalization and compression

Do not produce many ad hoc families that only cover the current small examples.

After candidate families are proposed, perform a compression pass:

1. group candidates by source constraints;
2. group by support pattern;
3. group by coefficient pattern;
4. group by c-MIR derivation route;
5. search for a common parameterized family containing several candidates as special cases.

If a more general family is proposed, it must still pass:

- exact instantiation matching;
- finite validity checking;
- derivation certificate checking.

Narrow families may remain only if:

- they have distinct derivation mechanisms;
- they occur under genuinely different parameter regimes;
- or no valid generalization has been found.

Otherwise, prefer the general family and record the narrow inequalities as special cases or coverage evidence.

## Anti-overfitting to computed facets

Computed facets from small instances are evidence, not templates to hard-code.

Do not create a symbolic family that merely repeats a concrete facet with renamed variables.

A family that depends on a concrete instance size or a concrete support must be treated as a local candidate.

Before reporting local candidates, attempt to generalize them using:

- arbitrary subset \(D\);
- complements such as \(J\setminus D\);
- intersections and set differences;
- threshold expressions such as \(b-|J\setminus D|\);
- coefficients obtained from residual, coefficient tightening, mixed MIR, or MIR-over-MIR derivations.

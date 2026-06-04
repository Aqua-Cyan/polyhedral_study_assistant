---
name: integer-hull-discovery
description: use this skill when analyzing integer linear sets, discovering convex hull descriptions, interpreting cddlib-generated facets, deriving valid inequalities with c-MIR, classifying facet families, or tracking proof obligations for integer hull descriptions.
---

# Integer Hull Discovery

When asked to analyze the convex hull of an integer linear set, do not guess the final convex hull description directly.

Use a staged research workflow. Treat computational evidence, valid inequality derivations, facetness proofs, and complete hull proofs as different levels of evidence.

## Required workflow

1. Formalize the set.
   - Define all variables, domains, index sets, parameters, and assumptions.
   - State whether index sets may overlap.
   - State whether parameters satisfy feasibility assumptions.
   - When a model is given in terms of overlapping index sets, do not force the user to reparameterize the model. Preserve the user's notation, but internally analyze useful set decompositions such as intersections, differences, nested cases, and symmetry classes. Any reparameterization must be explicitly labeled as an internal analysis device.

2. Identify the intended goal.
   - Complete convex hull description.
   - Valid inequality family.
   - Facet family.
   - Separation routine.
   - Extended formulation.
   - Computational exploration only.

3. Perform complexity triage when relevant.
   - Do not use NP-hardness as a reason to stop.
   - Use complexity only to decide whether a compact complete hull description is plausible.

4. Generate or request small instances.
   - Include boundary cases.
   - Include overlapping and non-overlapping index-set cases when relevant.
   - Include cases where parameters are tight, such as b = 1 or b = |J|.

   When the user gives a parametric integer linear set but does not provide concrete instances, propose a small-instance generation plan. The plan should include random small instances and structured edge cases. Do not assume the user has already selected cddlib instances.

5. Analyze cddlib-generated facets.
   - Normalize every inequality.
   - Record support, coefficient pattern, right-hand side, and symmetry class.
   - Distinguish original constraints, variable bounds, and nontrivial inequalities.

6. Search for derivations.
   - Identify source constraints involved in each facet.
   - Try nonnegative aggregation and coefficient tightening of original constraints.
   - Apply c-MIR or related mixed-integer rounding when appropriate.
   - Record the derivation as a certificate, not only as prose.

7. Generalize.
   - Turn repeated patterns into parameterized inequality families.
   - State all index conditions and parameter ranges.
   - Specify whether the family is valid, conjectural, facet-defining, or complete.

8. Verify.
   - Check whether candidate families cover all tested cddlib facets.
   - Search for violated integer points or fractional counterexamples.
   - Record unmatched facets and unresolved cases.

9. Identify the unmatched facets.
   - identify source constraints by support overlap;
   - check whether it is an aggregation of multiple original constraints with coefficient tightening;
   - check whether c-MIR or mixed-integer rounding can produce it;
   - check if it can be obtained by more than one pattern in c-MIR patterns, e.g., mixing after residual;
   - if a concrete derivation is found, generalize the same derivation to the symbolic model;
   - only if all attempts fail, place it in the unresolved section with an explicit failure reason.

10. Prove or label honestly.
   - Never call a description "the convex hull" unless completeness is proved.
   - If only small examples support it, label it "experimentally supported".
   - If validity is proved but completeness is not, say so explicitly.

## Required output sections

Use these sections unless the user requests a different format:

1. Problem formalization
2. Assumptions and edge cases
3. Small-instance plan
4. cddlib facet analysis plan
5. Candidate inequality families
6. c-MIR derivation attempts
7. Verification status
8. Proof obligations

## Status labels

Use these labels carefully:

- raw cddlib facet
- normalized
- original constraint
- variable bound
- matched by candidate family
- derived for this instance
- proved valid
- proved facet-defining
- experimentally supported
- conjectural
- complete hull proved

## Hard rule

Never claim that a system of inequalities gives the convex hull unless both inclusions are proved:

1. every integer feasible point satisfies the proposed inequalities;
2. every point satisfying the proposed inequalities belongs to the convex hull.

If the reverse inclusion is missing, state the missing proof obligation explicitly.

## Candidate family validation gate

When analyzing convex hulls of parametric integer linear sets, do not move directly from computed facets to a claimed symbolic family.

Use this pipeline:

computed facets
-> normalize facets
-> propose candidate symbolic family
-> instantiate family on concrete test instances
-> check exact matching against computed facets
-> check finite validity on enumerated feasible integer points
-> require a derivation certificate
-> write the family-first report
Exact matching requirement

A computed facet is covered by a symbolic family only if:

the family is instantiated with explicit parameter values;
the instantiated inequality is normalized;
the computed facet is normalized;
the two normalized inequalities are exactly equal.

Do not report coverage based only on visual similarity or coefficient resemblance.

Finite validity requirement:

Every candidate family instance must be checked against all enumerated feasible integer points in the tested small instance.

If a violating point is found, report the candidate as invalidated and include:

tested instance;
family parameter values;
instantiated inequality;
violating point;
violation value or violated side.

Invalidated candidates must not appear as proved or derived families.

Derivation certificate requirement:

A family can be labeled proved valid or derived only if it has a derivation certificate.

The certificate must use one or more documented derivation patterns:

residual inequality;
coefficient tightening;
aggregation;
c-MIR;
mixed MIR;
sequential MIR or MIR applied after MIR.

The certificate must include:

source constraints;
intermediate inequalities;
bound substitutions;
rounding or mixing step when used;
final symbolic inequality;
parameter conditions;
equality check against computed facets when claiming coverage.
Candidate status rule

Use these statuses carefully:

derived/proved valid: exact matching, finite validity, and derivation certificate are all available.
candidate: finite tests may support the family, but a derivation certificate is missing.
invalidated: a tested feasible point violates an instantiated inequality.
unresolved: no valid family or derivation attempt currently explains the facet.

A family that passes finite tests but lacks a derivation certificate must remain a candidate. A family that fails finite validity must be reported as invalidated with a counterexample.

## Computational backend rule

For small 0-1 instances, the assistant may use the project harness to enumerate feasible binary points and then compute the convex hull inequalities using the configured polyhedral backend.

The default backend is pycddlib, which converts point representations to inequality representations. It does not enumerate integer feasible points from symbolic constraints by itself.

Therefore, for parametric 0-1 sets:

1. instantiate small concrete index sets and parameters;
2. enumerate feasible 0-1 points for that concrete instance;
3. compute the convex hull of those points with pycddlib;
4. analyze the resulting inequalities.

## Do not report only concrete facets

For parametric integer sets, never make the main report a list of instance-level inequalities.

Concrete inequalities from cddlib/PORTA are evidence only. The main output must attempt to infer symbolic inequality families.

For each nontrivial concrete facet:

1. Rewrite it using the user's original notation.
2. Identify the source original constraints.
3. Derive it for the concrete instance using c-MIR, aggregation, or binary bound substitution.
4. Generalize the derivation to a symbolic family.
5. State the symbolic family before listing covered instances.

If no symbolic family is found, put the concrete facet in an "unmatched facets" section.

## Report organization rule

Organize research reports by inequality family, not by computational instance.

Instance-level output belongs only in a compact evidence table or appendix. Do not list all variable bounds or all concrete inequalities in the main body unless the user explicitly asks for raw computational output.
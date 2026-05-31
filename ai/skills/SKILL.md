---
name: integer-hull-discovery
description: use this skill when analyzing integer linear sets, discovering convex hull descriptions, interpreting PORTA-generated facets, deriving valid inequalities with c-MIR, classifying facet families, or tracking proof obligations for integer hull descriptions.
---

# Integer Hull Discovery

When asked to analyze the convex hull of an integer linear set, do not guess the final hull directly.

Use the following workflow:

1. Formalize the set, variables, parameters, integrality restrictions, and relaxation.
2. Clarify whether the goal is a complete hull description, a family of valid inequalities, a separation routine, or an extended formulation.
3. Perform complexity triage when relevant.
4. Use small instances and PORTA-generated facets as experimental evidence.
5. Normalize every inequality before interpreting it.
6. Classify facets by support, coefficient pattern, symmetry, and possible source constraints.
7. Try to derive candidate inequalities from aggregated original constraints using c-MIR.
8. Generalize repeated facet patterns into parameterized inequality families.
9. Clearly separate computational evidence from proof.
10. List unresolved proof obligations.

## Status labels

Use the following labels:

- `raw PORTA facet`
- `normalized`
- `matched by candidate family`
- `derived for this instance`
- `proved valid`
- `proved facet-defining`
- `experimentally supported`
- `conjectural`
- `complete hull proved`

## Hard rule

Never claim that a system of inequalities gives the convex hull unless both directions have been proved:

1. all integer feasible points satisfy the inequalities;
2. every point satisfying the inequalities belongs to the convex hull.

If only small-instance evidence is available, say that the description is experimentally supported, not proved.
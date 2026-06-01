# Research Workflow for Integer Hull Discovery

This workflow supports the discovery of convex hull descriptions for integer linear sets.

## 1. Formalization

For every problem, record:

- integer set S;
- continuous relaxation P;
- variable domains;
- parameter assumptions;
- index-set assumptions;
- target object, such as conv(S), a valid inequality family, or a facet family.

For set systems involving subsets J1, J2, ..., explicitly state whether these sets may overlap.

## 2. Small-instance generation

Generate a small-instance plan automatically when the user provides only a parametric model. Include both random instances and structured edge cases. Generate small instances that expose different structures:

- disjoint index sets;
- overlapping index sets;
- nested index sets;
- identical index sets;
- small right-hand sides;
- tight right-hand sides;
- infeasible parameter values, if useful as edge cases.

## 3. PORTA facet analysis

For each PORTA output inequality:

- normalize integer coefficients;
- identify support;
- identify whether it is a bound, original constraint, or nontrivial inequality;
- classify by coefficient pattern;
- classify by symmetry;
- record which instance produced it.

## 4. Derivation search

For every nontrivial inequality, try to identify:

- source constraints;
- aggregation multipliers;
- aggregated inequality;
- integer and continuous variables involved;
- c-MIR parameters;
- simplification steps;
- final inequality.

If no derivation is found, label the facet as unmatched.

## 5. Candidate family generalization

A candidate family must include:

- formal statement;
- index conditions;
- parameter restrictions;
- validity status;
- facetness status;
- examples matched;
- unmatched exceptions.

## 6. Verification

For every candidate family, check:

- no integer feasible point violates it in tested instances;
- the family matches expected PORTA facets;
- generated inequalities are not malformed;
- unmatched facets are reported.

## 7. Proof obligations

Separate the following levels:

- computational observation;
- valid for tested instances;
- generally valid;
- facet-defining;
- complete hull description.

A complete hull proof requires a proof of reverse inclusion.
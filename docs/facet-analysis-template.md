# Facet Analysis Protocol

This document defines how to analyze a computed facet and turn it into a symbolic inequality family.

The central rule is:

```text
Do not guess a broad family first.
Start from a concrete computed facet.
Derive that concrete facet.
Then generalize the derivation.
```

A computed facet is not considered understood until its source constraints and derivation route have been documented.

---

## 1. Input to facet analysis

For each computed facet, collect:

* normalized inequality;
* original unnormalized backend row, if available;
* variable order;
* source instance;
* support;
* coefficients by variable class;
* right-hand side;
* whether it is a bound, original constraint, or nontrivial inequality;
* whether it appears in multiple symmetric forms.

Example record:

```markdown
Facet:
\[
-x(D)+\alpha_1 y_1+\alpha_2 y_2\le 0.
\]

Support:
- \(x\)-support: \(D\)
- activation variables: \(y_1,y_2\)

Instance:
- \(J_1=...\)
- \(J_2=...\)
- \(b_1=...\)
- \(b_2=...\)
```

---

## 2. First classification

Classify the facet before deriving it.

Possible classes:

1. variable bound;
2. original constraint;
3. single-source residual inequality;
4. coefficient-tightened single-source inequality;
5. aggregation of multiple original constraints;
6. aggregation plus c-MIR;
7. mixed MIR;
8. MIR after MIR;
9. candidate interaction inequality;
10. unresolved.

This classification is provisional. It may change after derivation attempts.

---

## 3. Source-constraint identification

For every nontrivial facet, identify source constraints by support overlap.

For each original or derived source row, record:

* row name;
* symbolic form;
* concrete form;
* variables shared with the facet;
* variables in the row but not in the facet;
* variables in the facet but not in the row;
* whether upper/lower bounds could remove extra variables.

Example:

```markdown
Target facet:
\[
-x(D)+\alpha y\le0.
\]

Candidate source:
\[
x(J)\ge by.
\]

Shared support:
\[
D\cap J.
\]

Extra variables:
\[
J\setminus D.
\]
```

A source row is relevant if its extra variables can plausibly be eliminated or tightened using bounds, complementation, residualization, MIR, or mixing.

---

## 4. Required derivation attempts

Before reporting a facet as unresolved, try all relevant patterns below.

### 4.1 Residual attempt

Use this when a target resembles

[
x(D)\ge \alpha y.
]

From a source row

[
x(J)\ge by
]

and (D\subseteq J), let (E=J\setminus D). Since (x(E)\le |E|),

[
x(D)+x(E)\ge by
]

implies

[
x(D)\ge (b-|E|)y.
]

Check whether

[
\alpha=b-|J\setminus D|.
]

If yes, record a residual derivation certificate.

Important: do not restrict residual analysis to the case (\alpha=1). Larger residual coefficients are possible and must be checked.

---

### 4.2 Coefficient-tightening attempt

Use this when a source row or aggregate almost matches the target but has:

* extra variables;
* stronger coefficients than the target;
* weaker coefficients than the target;
* activation coefficients that need adjustment;
* asymmetric set differences.

Try:

* upper-bound substitution;
* lower-bound substitution;
* binary complementation;
* support restriction;
* tightening after residualization;
* tightening after aggregation;
* tightening after MIR.

Record:

```markdown
Pre-tightening inequality:
...

Variables eliminated:
...

Bounds used:
...

Tightened coefficients:
...

Final inequality:
...
```

No coefficient change is allowed without justification.

---

### 4.3 Aggregation plus c-MIR attempt

Use this when the facet appears to involve multiple original constraints.

Steps:

1. choose source constraints;
2. choose nonnegative multipliers;
3. form aggregate row;
4. identify integer variables and bounded variables;
5. apply c-MIR or MIR rounding;
6. simplify;
7. compare with the target facet.

Record:

```markdown
Source rows:
...

Multipliers:
...

Aggregate:
...

c-MIR step:
...

Simplified result:
...

Equality check:
...
```

If a variable is removed from the aggregate but not the target, state how it was removed.

---

### 4.4 Mixed-MIR attempt

Use mixed MIR only when the necessary base-inequality form is available.

For each base inequality, write:

[
f^i(x)+B g^i(x)\ge \pi_i.
]

Record:

* proof that (f^i(x)\ge0);
* proof that (g^i(x)\in\mathbb Z);
* (B);
* (\pi_i);
* (\tau_i=\lceil \pi_i/B\rceil);
* (\gamma_i=\pi_i-(\tau_i-1)B);
* ordering by (\gamma_i);
* common dominating function (\bar f);
* unsimplified mixed-MIR inequality;
* simplified final inequality.

Do not call ordinary linear combination of constraints mixed MIR.

If these objects cannot be identified, report mixed MIR as attempted but incomplete.

---

### 4.5 MIR after MIR attempt

A derived valid inequality may become a new source row.

After deriving one inequality, try using it as an input to another derivation pattern.

Examples:

```text
original row
  -> residual row
  -> aggregation with another residual row
  -> c-MIR
  -> target facet
```

```text
original row
  -> coefficient tightening
  -> MIR
  -> target facet
```

```text
original row
  -> residual row
  -> mixed MIR
  -> coefficient tightening
  -> target facet
```

Record every stage.

Do not collapse a multi-stage derivation into one vague statement such as “by c-MIR.”

---

## 5. Exact matching after derivation

After deriving a concrete inequality, check that it exactly matches the target facet.

Required check:

1. write the derived concrete inequality;
2. convert to the project's `LinearInequality` convention;
3. normalize it;
4. normalize the cddlib facet;
5. compare exact equality.

If equality fails, the derivation does not explain the facet.

---

## 6. Generalization after concrete derivation

Only after a concrete facet is derived should the assistant generalize.

The generalization must record:

* symbolic source constraints;
* symbolic subset choices;
* parameter conditions;
* symbolic derivation steps;
* final symbolic inequality;
* nontriviality conditions;
* validity status;
* facetness status;
* completeness status.

A generalization should not be broader than the derivation supports.

If a broad candidate is proposed, it must go through validation gates.

---

## 7. Candidate family validation

Every proposed symbolic family must pass the validation gates.

### Gate 1: exact instantiation matching

A candidate covers a computed facet only if an explicit instantiation of the symbolic family normalizes exactly to the computed facet.

Visual similarity is not enough.

### Gate 2: finite validity

For each tested instance and parameter choice, evaluate the candidate inequality on all enumerated feasible integer points.

If a feasible point violates the inequality, record:

* instance;
* parameter choice;
* inequality;
* violating point;
* violation value.

The candidate must be invalidated or refined.

### Gate 3: derivation certificate

A family may be labeled derived/proved only if it has a derivation certificate using the documented patterns.

Finite validity is not a proof.

Exact facet matching is not a proof.

---

## 8. Handling invalidated candidates

Invalidated candidates should not be discarded silently.

They should be reported because they help refine conditions.

For each invalidated candidate, record:

* original candidate statement;
* counterexample;
* failed parameter condition;
* possible refined conditions;
* next attempted derivation route.

Example:

```markdown
The candidate \(x(S)\ge r_1(S)y_1+r_2(S)y_2\) failed for the following feasible point...

This suggests that the two residual demands cannot simply be added when the same \(x\)-support is counted twice.
```

---

## 9. Handling unresolved facets

A facet may be unresolved only after all relevant derivation attempts have been documented.

For each unresolved facet, report:

* target facet;
* source constraints tried;
* residual result;
* coefficient-tightening result;
* aggregation+c-MIR result;
* mixed-MIR result;
* MIR-after-MIR result;
* why each failed or remains incomplete;
* next action.

If many unresolved facets share a pattern, group them by signature and analyze the signature.

---

## 10. Facet signature templates

When grouping facets, use signatures such as:

```text
support size
support location
activation variables present
activation coefficients
source rows involved
overlap with each source row
```

For two-set models, useful signatures include:

* support in (J_1\setminus J_2);
* support in (J_2\setminus J_1);
* support in (J_1\cap J_2);
* support in (J_1\cup J_2);
* one activation variable;
* both activation variables;
* coefficients (y_1+y_2);
* coefficients (2y_1+y_2);
* coefficients (y_1+2y_2);
* coefficients (2y_1+2y_2).

A signature is not a proof. It is only a guide for derivation attempts.

---

## 11. Completion rule

Facet analysis for one run is complete only when every computed nontrivial facet is in exactly one of these states:

1. variable bound;
2. original constraint;
3. covered by a derived/proved symbolic family;
4. covered by a candidate family but derivation missing;
5. invalidated candidate evidence;
6. unresolved with documented failed derivation attempts.

If a facet is simply omitted, the analysis is incomplete.

If a facet is labeled candidate but no derivation was attempted, the analysis is incomplete.

If a facet is labeled covered but exact instantiation matching was not performed, the analysis is incomplete.

---

## 12. Checklist for each nontrivial facet

Before moving on from a facet, answer:

```markdown
- [ ] Is the facet normalized?
- [ ] Is it a bound or original constraint?
- [ ] What source constraints overlap its support?
- [ ] Was residual derivation tried?
- [ ] Was coefficient tightening tried?
- [ ] Was aggregation+c-MIR tried?
- [ ] Was mixed MIR tried, if applicable?
- [ ] Was MIR-after-MIR tried?
- [ ] If a derivation succeeded, was it generalized symbolically?
- [ ] Was exact matching checked?
- [ ] Was finite validity checked?
- [ ] Is the status label correct?
- [ ] Is the next action clear?
```

This checklist should be used before writing the final report.

## MIR-over-MIR exploration rule

When a computed facet is not explained by applying one pattern directly to the original constraints, do not stop.

A valid inequality derived from the original constraints may become a new source row. The assistant should explore derivation chains of the form:

```text
original constraints
→ residual / coefficient tightening / MIR / mixed MIR
→ intermediate valid inequalities
→ another residual / coefficient tightening / MIR / mixed MIR step
→ target facet
```

The intermediate inequality does not need to be a facet. It only needs to be valid and have a documented derivation certificate.

### Required search behavior

For every unresolved facet, try at least the following MIR-over-MIR routes when relevant:

1. **Residual then residual/mixing**

   Derive residual inequalities from one or more original source constraints.
   Then treat those residual inequalities as new source rows and try to combine them using mixed MIR, aggregation+c-MIR, coefficient tightening, or support relaxation.

2. **Residual then support relaxation**

   If a residual inequality is first derived on (D\cap J), check whether it can be relaxed to a larger target support (D) using monotonicity of nonnegative binary variables:

   [
   x(D)\ge x(D\cap J).
   ]

   Then use the relaxed row as a new source inequality.

3. **Coefficient tightening then MIR**

   If a source row can be tightened first, use the tightened row as the base row for a later MIR or mixed-MIR step.

4. **Mixed MIR then coefficient tightening**

   If mixed MIR produces an inequality with the correct structure but weak coefficients or extra variables, try coefficient tightening afterward.

5. **Candidate row generation**

   If a derivation attempt produces a valid but non-facet intermediate inequality, keep it in a temporary source-row pool. Try using it in later derivation attempts before declaring the target facet unresolved.

### Required documentation

For every MIR-over-MIR chain, record:

* original source constraints;
* each intermediate inequality;
* which derivation pattern produced each intermediate inequality;
* why each intermediate inequality is valid;
* how the intermediate inequality is used as a new source row;
* final reconstructed inequality;
* exact matching result against the computed facet;
* finite validity result;
* remaining proof obligations.

Do not write only “by c-MIR” or “by MIR over MIR.” The derivation chain must be explicit enough that a human researcher can check every step.

### Important distinction

The generic c-MIR attemptor is only a scaffold. If it returns `needs_problem_specific_derivation`, the assistant must continue reasoning mathematically. A failed generic attempt does not mean the target facet cannot be derived.

Unresolved means:

all relevant residual, tightening, aggregation+c-MIR, mixed-MIR,
and MIR-over-MIR chains were attempted and documented.

It does not mean:

the first direct residual or aggregation attempt failed.

## From facet signatures to general families

Facet signatures are not final families.

When several facets share a signature, the assistant must attempt to identify a general family.

For each group of similar facets:

1. list the common source constraints;
2. identify the varying supports;
3. express the support using a symbolic subset such as \(D\);
4. express missing variables using complements such as \(J\setminus D\);
5. express coefficients using parameter formulas such as \(b-|J\setminus D|\);
6. test whether the general formula instantiates back to the concrete facets;
7. check finite validity;
8. attempt a derivation certificate.

Do not create separate families for each support size if a single subset-parameterized family explains them.

## Larger-instance pressure test

If a proposed family is based only on tiny instances, run larger or more varied instances before reporting it as stable.

The pressure test should include:

- larger supports;
- proper subsets of different sizes;
- asymmetric thresholds;
- overlap regions of size at least 2 when applicable;
- nested and identical cases.

If the family fails, record the counterexample and refine the parameter conditions.

If it survives but lacks a derivation, keep it as a candidate.
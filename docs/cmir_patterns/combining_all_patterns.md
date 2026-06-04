# Combined Derivation Patterns for Valid Inequalities

## Purpose

This guide explains how to combine several valid-inequality derivation patterns when analyzing computed facets of a parametric integer linear set.

The goal is not to merely list concrete facets. The goal is to explain a concrete facet by a derivation, then generalize the same derivation to a symbolic valid inequality family.

The main patterns covered here are:

1. residual inequalities;
2. coefficient tightening;
3. mixed MIR inequalities, also called mixing mixed-integer inequalities;
4. combinations of the above.

A computed facet should be reported as unresolved only after these derivation attempts have been tried and documented.

---

## General derivation workflow

Given a computed facet (F), follow this sequence.

### Step 1. Normalize the concrete facet

Write the facet in a consistent form, for example

[
a^\top x + \alpha^\top y \le \beta.
]

Record:

* support of the facet;
* coefficients on binary variables;
* coefficients on continuous or integer variables;
* right-hand side;
* which original constraints contain the variables in the support.

### Step 2. Identify candidate source constraints

Find original constraints whose supports overlap the target facet. For each candidate source constraint, record:

* symbolic form;
* concrete instantiated form;
* variables shared with the facet;
* variables present in the source but absent from the facet;
* variables present in the facet but absent from the source.

A source constraint is useful if its variables can plausibly be transformed into the target support by:

* residualization;
* variable upper-bound substitution;
* coefficient tightening;
* complementation;
* MIR;
* mixed MIR;
* aggregation followed by one of the above.

### Step 3. Try simple residual derivations first

If the facet has the form

[
-x(D)+\alpha y \le 0
]

or equivalently

[
x(D)\ge \alpha y,
]

check whether it comes from a single activation lower-bound constraint

[
x(J)\ge b y.
]

Let (E=J\setminus D). Since (x(E)\le |E|) for binary (x), we obtain

[
x(D)+x(E)\ge by
]

and therefore

[
x(D)\ge (b-|E|)y.
]

Thus the facet is explained by the residual pattern if

[
\alpha=b-|J\setminus D|>0.
]

If this succeeds, produce the symbolic family:

[
x(D)\ge (b-|J\setminus D|)y,
\qquad
D\subseteq J,\quad b-|J\setminus D|>0.
]

Do not label such a facet as unmatched.

### Step 4. Try coefficient tightening

If a facet contains variables from two or more source constraints and some variables appear with coefficients that are smaller than those obtained by direct addition, try coefficient tightening.

A typical situation is a pair of constraints such as

[
x(J_r)\ge b_r y_r
]

and

[
x(J_i)\le (|J_i|-b_i+1)y_i+b_i-1.
]

Select subsets

[
D_1\subseteq J_r,\qquad D_2\subseteq J_i.
]

Use residual inequalities or restrictions of the two source constraints to obtain inequalities involving (x(D_1)) and (x(D_2)). Add these inequalities and rearrange them so that the target support appears.

For example, if one has

[
x(D_1)\ge (b_r-|J_r\setminus D_1|)y_r
]

and

[
(|D_2|-b_i+1)y_i+b_i-1\ge x(D_2),
]

then adding gives

[
x(D_1)+(|D_2|-b_i+1)y_i+b_i-1
\ge
(b_r-|J_r\setminus D_1|)y_r+x(D_2).
]

This can be rewritten as

[
(|D_2|-b_i+1)y_i
+
(b_r-|J_r\setminus D_1|)(1-y_r)
\ge
x(D_2)-x(D_1)-b_i+1+b_r-|J_r\setminus D_1|.
]

If the target only uses the asymmetric support

[
D_2\setminus D_1
\quad\text{and}\quad
D_1\setminus D_2,
]

replace

[
x(D_2)-x(D_1)
]

by

[
x(D_2\setminus D_1)-x(D_1\setminus D_2).
]

Then strengthen the coefficients of (y_i) and (1-y_r) whenever the binary structure allows it. In the MALP-style tightening pattern, this gives a strengthened inequality of the form

[
\lambda y_i+\mu(1-y_r)
\ge
x(D_2\setminus D_1)-x(D_1\setminus D_2)
-b_i+1+b_r-|J_r\setminus D_1|,
]

where

[
\lambda
=======

\min{
|D_2|-b_i+1,,
|D_1\cup D_2|-b_i+1+b_r-|J_r|
},
]

and

[
\mu
===

\min{
b_r-|J_r\setminus D_1|,,
|D_1\cup D_2|-b_i+1+b_r-|J_r|
}.
]

A coefficient-tightening derivation certificate must record:

* the two source constraints;
* chosen subsets (D_1,D_2);
* the pre-tightening inequality;
* which coefficients are tightened;
* the formula for the tightened coefficients;
* the resulting symbolic inequality;
* the conditions under which the inequality is nontrivial.

### Step 5. Try mixed MIR only after identifying valid base inequalities

Do not treat mixing as ordinary addition of original constraints.

The mixed MIR procedure starts from a collection of base mixed-integer inequalities of the form

[
f^i(x)+B g^i(x)\ge \pi_i,
\qquad i\in I,
]

where

[
f^i(x)\ge 0,
\qquad
g^i(x)\in \mathbb Z.
]

For each base inequality, define

[
\tau_i=\left\lceil\frac{\pi_i}{B}\right\rceil,
]

and

[
\gamma_i=\pi_i-(\tau_i-1)B,
\qquad 0<\gamma_i\le B.
]

The corresponding simple MIR inequality is

[
f^i(x)\ge \gamma_i(\tau_i-g^i(x)).
]

A mixed MIR inequality combines these MIR right-hand sides under a common dominating function (\bar f) satisfying

[
\bar f(x)\ge f^i(x)
\quad\text{for all selected }i.
]

After sorting the selected inequalities so that

[
0=\gamma_0\le \gamma_1\le \gamma_2\le \cdots \le \gamma_n,
]

one mixed MIR inequality is

[
\bar f(x)
\ge
\sum_{i=1}^n
(\gamma_i-\gamma_{i-1})(\tau_i-g^i(x)).
]

A second mixed MIR inequality is

[
\bar f(x)
\ge
\sum_{i=1}^n
(\gamma_i-\gamma_{i-1})(\tau_i-g^i(x))
+
(B-\gamma_n)(\tau_1-g^1(x)-1).
]

When there is only one selected base inequality, the first inequality reduces to the simple MIR inequality, while the second recovers the original base inequality.

Use mixed MIR only when you can provide:

* the base inequalities;
* the common value (B), or a justified scaling to obtain compatible (B)'s;
* the integer functions (g^i(x));
* the nonnegative functions (f^i(x));
* the values (\tau_i) and (\gamma_i);
* the ordering by (\gamma_i);
* a common (\bar f(x)) dominating the selected (f^i(x));
* the resulting mixed MIR inequality.

### Step 6. Normalize base inequalities before applying mixed MIR

If a candidate base inequality does not satisfy (f^i(x)\ge 0), look for a lower bound

[
f^i(x)\ge L_i.
]

Then rewrite it as

[
(f^i(x)-L_i)+B g^i(x)\ge \pi_i-L_i,
]

so that the new nonnegative part is

[
\hat f^i(x)=f^i(x)-L_i\ge 0.
]

Then compute the MIR and mixed MIR parameters using the shifted right-hand side.

If base inequalities have different (B_i)'s, do not apply the basic common-(B) formula directly. Instead, try one of the following:

1. scale base inequalities so that compatible (B)'s are obtained;
2. relax smaller (B_i)'s upward when valid;
3. check whether (\min_i B_i\ge \max_i \gamma_i);
4. if none of these holds, report that the basic mixed MIR pattern does not apply.

### Step 7. Consider independent groups only with a valid (\bar f)

Sometimes base inequalities can be partitioned into independent groups with respect to (\bar f).

This is not the same as arbitrary grouping. It requires a dominance condition such as

[
\bar f(x)\ge \sum_j f_j^*(x),
]

where (f_j^*(x)) dominates the (f)-parts in group (j).

Only then may one use the stronger independent-group mixing pattern.

A derivation using independent groups must record:

* the groups of base inequalities;
* the function (f_j^*) for each group;
* the global (\bar f);
* the ordering of the mixed terms;
* the coefficient system or lifting order used;
* the final inequality.

If these objects cannot be identified, do not claim an independent mixing derivation.

---

## How to combine the patterns

The patterns can be combined in several ways. The correct order depends on the target facet.

### Route A: residual first, then coefficient tightening

Use this route when the target facet resembles a strengthened form of one or two activation constraints.

1. Apply residual inequalities to one or more source constraints.
2. Add the residual inequalities if the target facet involves multiple supports.
3. Rearrange to expose the target support.
4. Tighten coefficients using binary variable bounds.
5. Generalize the result symbolically.

This is often useful for 0-1 sets with lower-bound and upper-bound activation constraints.

### Route B: coefficient tightening first, then residualization

Use this route when the target facet contains asymmetric set differences such as

[
x(D_2\setminus D_1)-x(D_1\setminus D_2).
]

1. Combine source constraints to produce a preliminary inequality.
2. Separate common and non-common variables.
3. Remove or bound variables outside the target support.
4. Tighten coefficients on binary activation variables.
5. Express the result as a symbolic family.

### Route C: base-inequality construction, then mixed MIR

Use this route when the target facet appears to combine several MIR inequalities rather than merely residualizing a single constraint.

1. Identify several base inequalities of the form

   [
   f^i(x)+B g^i(x)\ge \pi_i.
   ]

2. Verify

   [
   f^i(x)\ge 0,
   \qquad
   g^i(x)\in\mathbb Z.
   ]

3. If necessary, shift or scale the base inequalities.

4. Compute

   [
   \tau_i=\left\lceil\frac{\pi_i}{B}\right\rceil,
   \qquad
   \gamma_i=\pi_i-(\tau_i-1)B.
   ]

5. Form the simple MIR inequalities.

6. Choose a valid common (\bar f(x)).

7. Sort by (\gamma_i).

8. Apply the mixed MIR formula.

9. Simplify the result.

10. Compare the simplified symbolic inequality with the concrete facet.

This route should not be described as mixing unless all base-inequality and (\bar f) requirements are documented.

### Route D: mixed MIR followed by coefficient tightening

Use this route when the mixed MIR inequality has the correct general structure but coefficients are not yet as strong as the computed facet.

1. Derive a valid mixed MIR inequality.
2. Compare it with the target facet.
3. Identify variables whose coefficients can be strengthened using binary bounds or problem-specific dominance.
4. Apply coefficient tightening.
5. Record both the pre-tightened mixed MIR inequality and the tightened final inequality.

### Route E: coefficient tightening followed by mixed MIR

Use this route when the natural base inequalities are weak, but tightened or shifted versions provide better MIR residues.

1. Start from candidate source constraints.

2. Apply coefficient tightening, shifting, or relaxation to construct better base inequalities.

3. Rewrite the tightened inequalities in the form

   [
   f^i(x)+B g^i(x)\ge \pi_i.
   ]

4. Apply the mixed MIR procedure.

5. Generalize the resulting inequality.

---

## Required derivation certificate

Every successful symbolic family must include a derivation certificate.

### For residual inequalities

Record:

* source constraint (x(J)\ge by);
* subset (D);
* complement (E=J\setminus D);
* bound (x(E)\le |E|);
* resulting inequality;
* nontriviality condition.

### For coefficient tightening

Record:

* source constraints;
* chosen subsets;
* pre-tightening inequality;
* tightened coefficients;
* reason the coefficient reduction is valid;
* symbolic final inequality.

### For mixed MIR

Record:

* base inequalities;
* (f^i(x)), (g^i(x)), (B), and (\pi_i);
* proof that (f^i(x)\ge0) and (g^i(x)\in\mathbb Z);
* (\tau_i) and (\gamma_i);
* selected subset of base inequalities;
* ordering by (\gamma_i);
* common dominating (\bar f(x));
* whether type (4), type (5), or an independent-group extension is used;
* final symbolic inequality.

### For failed attempts

Record:

* target facet;
* source constraints tried;
* why residualization failed;
* why coefficient tightening failed;
* why mixed MIR did not apply;
* what additional structure would be needed.

---

## Reporting rule

The final research report must be organized by symbolic inequality family, not by individual computational instance.

Computed facets should appear only as:

* coverage evidence;
* examples of substitutions into symbolic families;
* unresolved targets after documented derivation attempts;
* appendix data.

A concrete facet must not be labeled merely as "unmatched" until the residual, coefficient-tightening, and mixed MIR derivation attempts have been documented.

## MIR-over-MIR and derived-row reuse

Many useful inequalities are not obtained by applying a single pattern directly to the original constraints.

A derivation may require several rounds. In such cases, every valid inequality produced in an earlier round may be reused as a new source row in a later round.

This is called here **MIR-over-MIR** or **derived-row reuse**.

### General principle

If a row (R) is valid for the integer set and has a valid derivation certificate, then (R) may be used as a source row in a later derivation attempt.

For example:

```text
original row
→ residual inequality
→ relaxed residual inequality on a larger support
→ mixed MIR with another residual inequality
→ coefficient tightening
→ target facet
```

The intermediate row does not need to be facet-defining. Validity is enough.

### Common MIR-over-MIR routes

#### Route F: residual rows as mixed-MIR base rows

1. Start from multiple activation constraints.
2. Derive residual inequalities from each one.
3. If necessary, relax the left-hand sides to a common support.
4. Treat the resulting residual inequalities as new base rows.
5. Apply mixed MIR, aggregation+c-MIR, or coefficient tightening.
6. Compare the final inequality with the computed target facet.

This route is especially useful when a target facet has one common (x)-support and multiple activation variables.

#### Route G: residual then support relaxation

Suppose a source row gives

[
x(D\cap J)\ge r y.
]

If (D\cap J\subseteq D) and (x\ge 0), then

[
x(D)\ge x(D\cap J)\ge r y.
]

Thus one can derive the relaxed row

[
x(D)\ge r y.
]

This relaxed row may be weaker than the original residual inequality, but it can become useful because several relaxed rows may now have a common left-hand side.

#### Route H: derived row then coefficient tightening

If an intermediate row has the right variables but weak coefficients, try coefficient tightening. Record both the pre-tightening and post-tightening forms.

#### Route I: mixed MIR then further MIR

If mixed MIR produces a valid inequality that still does not match the computed facet, treat it as an intermediate valid row and try applying another MIR or tightening step.

### Search guidance for the assistant

When a computed facet is not matched:

1. Do not only try patterns on the original constraints.
2. Generate intermediate valid inequalities using residual, tightening, aggregation, or mixed MIR.
3. Add those intermediate inequalities to the source-row pool.
4. Retry the derivation patterns using this expanded source-row pool.
5. Continue for a small bounded depth, such as depth 2 or depth 3, before declaring the facet unresolved.

### Required certificate for MIR-over-MIR

A MIR-over-MIR derivation must list each stage:

```text
Stage 0: original source constraints
Stage 1: first derived valid inequality
Stage 2: second derived valid inequality
...
Final stage: target inequality
```

For each stage, record:

* derivation pattern used;
* source rows used;
* formula before simplification;
* formula after simplification;
* validity justification;
* whether the final row exactly matches the computed facet.

A broad symbolic family discovered through MIR-over-MIR must still pass:

1. exact instantiation matching;
2. finite validity checking;
3. derivation certificate checking.


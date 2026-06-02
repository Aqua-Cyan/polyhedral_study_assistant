# c-MIR / derivation playbook

## Pattern 1: residual lower-bound inequality

Source:
\[
x(J)\ge by,\quad x_j\in\{0,1\}.
\]

For \(D\subseteq J\), let \(E=J\setminus D\). Since \(x(E)\le |E|\),

\[
x(D)\ge (b-|E|)y.
\]

Use this pattern whenever a computed facet has the form:

\[
-x(D)+\alpha y\le 0.
\]

Check \(\alpha=b-|J\setminus D|\).

## Pattern 2: aggregation of two lower-bound constraints

Source:
\[
x(J_1)\ge b_1y_1,\quad x(J_2)\ge b_2y_2.
\]

For nonnegative multipliers \(\lambda_1,\lambda_2\), aggregate:

\[
\lambda_1 x(J_1)+\lambda_2 x(J_2)\ge
\lambda_1 b_1 y_1+\lambda_2 b_2y_2.
\]

Then use binary upper bounds to eliminate variables outside the target support.

## Pattern 3: target-support tightening

Given a target facet supported on \(D\), variables outside \(D\) must be eliminated using:
- upper bounds \(x_j\le1\),
- lower bounds \(x_j\ge0\),
- complementing \(x_j=1-z_j\),
- or MIR/c-MIR rounding after aggregation.

If a variable appears in the aggregate but not in the target, record how it is eliminated.

## Required derivation output

Every derivation attempt must report:
- target facet;
- source constraints;
- multipliers;
- variables eliminated;
- rounding/tightening step;
- resulting symbolic family;
- status.
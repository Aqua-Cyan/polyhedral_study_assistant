# MALP

We study the 0-1 set

\[
\mathcal T=
\{(x,y_1,y_2)\in\{0,1\}^{|\mathcal J_1\cup\mathcal J_2|+2}:
x(\mathcal J_1)\ge b_1y_1,\ 
x(\mathcal J_2)\ge b_2y_2
\}.
\]

Here \(x(\mathcal J)=\sum_{j\in\mathcal J}x_j\).

## Parameters

- \(\mathcal J_1,\mathcal J_2\): finite index sets.
- \(b_1,b_2\): positive integers.
- \(x_j\in\{0,1\}\) for \(j\in \mathcal J_1\cup\mathcal J_2\).
- \(y_1,y_2\in\{0,1\}\).

## Research purpose

This example is used to test the integer-hull discovery workflow on a small structured 0-1 set with two activation-type lower-bound constraints.

## Open assumptions

The workflow should explicitly determine or test:

- whether \(\mathcal J_1\) and \(\mathcal J_2\) are disjoint, overlapping, nested, or identical;
- whether \(1\le b_k\le |\mathcal J_k|\);
- whether overlapping variables create interaction inequalities beyond the two original constraints and variable bounds.

## Status

No convex hull description is assumed at this stage.
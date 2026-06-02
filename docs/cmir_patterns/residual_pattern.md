# Residual Inequality Pattern

## Description

Residual inequalities are derived from single activation constraints of the form:

\[
x(J) \ge b \, y
\]

where \(x_j \in \{0,1\}\) and \(y \in \{0,1\}\).

For any subset \(D \subseteq J\), let \(E = J \setminus D\). Using the upper bounds on binary variables \(x(E) \le |E|\), we can derive:

\[
x(D) \ge (b - |E|) y
\]

provided that \(b - |E| > 0\).

## Step-by-Step Derivation

1. Identify the activation constraint \(x(J) \ge b y\).
2. Choose a subset \(D\) of the support \(J\) for which you want to derive the residual inequality.
3. Let \(E = J \setminus D\).
4. Apply the upper bounds: \(x(E) \le |E|\).
5. Rearrange to obtain \(x(D) \ge (b - |E|) y\).
6. Verify that the derived inequality is nontrivial (\(b - |E| > 0\)).

## Example

Given \(J = \{1,2,3\}\) and \(b = 2\), for \(D = \{1,2\}\), we have \(E = \{3\}\):

\[
x_1 + x_2 + x_3 \ge 2 y \implies x_1 + x_2 \ge (2-1) y = y
\]

This gives the residual inequality \(x_1 + x_2 \ge y\).

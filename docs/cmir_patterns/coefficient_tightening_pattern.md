# Coefficient Tightening Pattern (Updated)

## Description

Coefficient strengthening (tightening) is a procedure to derive stronger valid inequalities
from existing constraints by combining them and adjusting coefficients according to variable bounds.

It is particularly useful for 0-1 integer sets with both lower and upper bounds.

## Step-by-Step Template

1. **Identify source constraints**
   - Lower-bound constraint: \(x(J_r) \ge b_r y_r\)
   - Upper-bound constraint: \(x(J_i) \le (|J_i| - b_i + 1)y_i + b_i - 1\)
2. **Select substructures**
   - Pick subsets \(D_1 \subseteq J_r\) and \(D_2 \subseteq J_i\) relevant to the target inequality.
3. **Combine constraints**
   - Add or subtract the two inequalities to target variables in \(D_1, D_2\):
     \[
     x(D_1) \text{ and } x(D_2)
     \]
4. **Tighten coefficients**
   - Apply variable upper bounds (\(x_j \le 1\)) and lower bounds (\(x_j \ge 0\)) to reduce coefficients of variables outside the target subset.
   - Compute adjusted coefficients using minimums or residual capacities:
     \[
     \lambda_1 = \min\{|D_2|-b_i+1, |D_1 \cup D_2| - b_i + 1 + b_r - |J_r|\}
     \]
     \[
     \mu_1 = \min\{b_r - |J_r \setminus D_1|, |D_1 \cup D_2| - b_i + 1 + b_r - |J_r|\}
     \]
5. **Form the tightened inequality**
   - Example form after tightening:
     \[
     \lambda_1 y_i + \mu_1 (1 - y_r) \ge x(D_2 \setminus D_1) - x(D_1 \setminus D_2) - b_i + 1 + b_r - |J_r \setminus D_1|
     \]
6. **Check validity**
   - Ensure the inequality is valid for all feasible 0-1 assignments.
7. **Generalization**
   - Once derived for a concrete instance, abstract the derivation to symbolic form to define a general family of inequalities.

## Notes

- This method can be combined with other derivation patterns, such as residual inequalities or mixing inequalities.
- Tightening is essential to remove slack in coefficients and produce strong valid inequalities.
- The approach can be applied iteratively to multiple source constraints to generate complex facets.

## Example

Given:

\[
x(J_r) \ge b_r y_r, \quad x(J_i) \le (|J_i|-b_i+1) y_i + b_i - 1
\]

Pick subsets \(D_1 \subseteq J_r\), \(D_2 \subseteq J_i\), combine, tighten coefficients as above,
and derive the inequality:

\[
\lambda_1 y_i + \mu_1 (1 - y_r) \ge x(D_2 \setminus D_1) - x(D_1 \setminus D_2) - b_i + 1 + b_r - |J_r \setminus D_1|
\]

which is valid and can be generalized to symbolic inequalities for the parametric problem.
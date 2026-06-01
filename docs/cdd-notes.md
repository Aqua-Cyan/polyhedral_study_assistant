# cddlib / pycddlib Notes

pycddlib is the preferred computational backend for the first version of this project.

It provides Python bindings for cddlib, which implements the double description method. The backend is used for converting between V-representations and H-representations of convex polyhedra.

## Intended use in this project

The main workflow is:

1. Generate small concrete 0-1 instances from a parametric integer linear set.
2. Enumerate feasible 0-1 points for the small instance.
3. Pass these points to pycddlib as a generator representation.
4. Compute the H-representation of their convex hull.
5. Convert pycddlib inequalities to PSA's `LinearInequality` format.
6. Normalize, classify, and report the resulting inequalities.

## Important limitation

pycddlib does not enumerate 0-1 feasible points from symbolic integer constraints.

For small 0-1 instances, this project initially uses brute-force enumeration. This is acceptable because the intended use is small-instance facet discovery, not large-scale optimization.

## Representation convention

pycddlib uses rows of the form

```text
[b, a1, ..., an]

to represent

0 <= b + a1 x1 + ... + an xn.

PSA uses the convention

a x <= rhs.

Therefore, a pycddlib row [b, a1, ..., an] is converted to

(-a1, ..., -an) x <= b.
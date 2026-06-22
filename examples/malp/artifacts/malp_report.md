# MALP convex-hull study report

## Scope and limitations

- This report uses exhaustive feasible-point enumeration plus pycddlib convex-hull computation on staged small-to-medium MALP instances.
- Tested instances: 15 staged cases; nontrivial computed facets recorded: 195.
- The current cdd backend skips equations returned by pycddlib; if equations occur, the report must state this backend limitation explicitly.
- Unresolved facets remaining after the current loop: 47.
- Candidate families remaining without derivation certificates: 1.
- No complete convex-hull description is claimed; reverse inclusion has not been proved.

## Model

We study the 0-1 set

\[
\mathcal T=
\{(x,y_1,y_2)\in\{0,1\}^{|J_1\cup J_2|+2}: x(J_1)\ge b_1 y_1,\ x(J_2)\ge b_2 y_2\}.
\]

The analysis uses the region decomposition
\[
J_1\setminus J_2,\qquad J_1\cap J_2,\qquad J_2\setminus J_1,
\]
only as an internal device for facet signatures and candidate-family compression; the reported families remain stated in the original notation whenever possible.

## Derived or proved symbolic inequality families

Families in this section have passed the derivation-certificate gate. When coverage is claimed, the concrete facets must be exactly reproduced by instantiating the symbolic family and normalizing the resulting inequality.

### Residual family for J1

#### Symbolic statement

x(D) >= (b_1 - |J_1 \ D|) y_1

#### Parameter conditions

- D subset J_1
- b_1 - |J_1 \ D| > 0

#### Derivation certificate

- Source row: x(J_k) >= b_k y_k.
- Let E = J_k \ D and use x(E) <= |E|.
- Then x(D) >= (b_k - |J_k \ D|) y_k.
- Gate 1 passed on the matched concrete instances by exact normalized equality.
- Gate 2 passed for the reported concrete matches on enumerated feasible points.
- Gate 3 passed by the residual derivation certificate.

#### Status

- validity: `proved valid for the documented residual derivation route`
- facetness: `facetness unproved`
- completeness: `complete hull not claimed`

#### Covered computed facets

- `-x_a - x_b + y_1 <= 0` (source: disjoint_3x3; source='j1', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_1 <= 0` (source: disjoint_3x3; source='j1', subset=('a', 'c'), residual=1)
- `-x_b - x_c + y_1 <= 0` (source: disjoint_3x3; source='j1', subset=('b', 'c'), residual=1)
- `-x_a - x_b + y_1 <= 0` (source: overlap_1; source='j1', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_1 <= 0` (source: overlap_1; source='j1', subset=('a', 'c'), residual=1)
- `-x_b - x_c + y_1 <= 0` (source: overlap_1; source='j1', subset=('b', 'c'), residual=1)
- `-x_a - x_b - x_c + y_1 <= 0` (source: overlap_2; source='j1', subset=('a', 'b', 'c'), residual=1)
- `-x_a - x_b - x_d + y_1 <= 0` (source: overlap_2; source='j1', subset=('a', 'b', 'd'), residual=1)
- `-x_a - x_c - x_d + y_1 <= 0` (source: overlap_2; source='j1', subset=('a', 'c', 'd'), residual=1)
- `-x_b - x_c - x_d + y_1 <= 0` (source: overlap_2; source='j1', subset=('b', 'c', 'd'), residual=1)
- `-x_a - x_b + y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('a', 'c'), residual=1)
- `-x_a - x_d + y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('a', 'd'), residual=1)
- `-x_b - x_c + y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('b', 'c'), residual=1)
- `-x_b - x_d + y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('b', 'd'), residual=1)
- `-x_c - x_d + y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('c', 'd'), residual=1)
- `-x_a - x_b - x_c + 2 y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('a', 'b', 'c'), residual=2)
- `-x_a - x_b - x_d + 2 y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('a', 'b', 'd'), residual=2)
- `-x_a - x_c - x_d + 2 y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('a', 'c', 'd'), residual=2)
- `-x_b - x_c - x_d + 2 y_1 <= 0` (source: nested_j2_in_j1; source='j1', subset=('b', 'c', 'd'), residual=2)
- `-x_a + y_1 <= 0` (source: boundary_full; source='j1', subset=('a',), residual=1)
- `-x_b + y_1 <= 0` (source: boundary_full; source='j1', subset=('b',), residual=1)
- `-x_c + y_1 <= 0` (source: boundary_full; source='j1', subset=('c',), residual=1)
- `-x_a - x_b - x_c + y_1 <= 0` (source: medium_overlap_5; source='j1', subset=('a', 'b', 'c'), residual=1)
- `-x_a - x_b - x_d + y_1 <= 0` (source: medium_overlap_5; source='j1', subset=('a', 'b', 'd'), residual=1)
- `-x_a - x_c - x_d + y_1 <= 0` (source: medium_overlap_5; source='j1', subset=('a', 'c', 'd'), residual=1)
- `-x_b - x_c - x_d + y_1 <= 0` (source: medium_overlap_5; source='j1', subset=('b', 'c', 'd'), residual=1)
- `-x_a - x_b + y_1 <= 0` (source: medium_nested_6; source='j1', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_1 <= 0` (source: medium_nested_6; source='j1', subset=('a', 'c'), residual=1)
- `-x_b - x_c + y_1 <= 0` (source: medium_nested_6; source='j1', subset=('b', 'c'), residual=1)
- `-x_a - x_b - x_c + y_1 <= 0` (source: sweep_422; source='j1', subset=('a', 'b', 'c'), residual=1)
- `-x_a - x_b - x_d + y_1 <= 0` (source: sweep_422; source='j1', subset=('a', 'b', 'd'), residual=1)
- `-x_a - x_c - x_d + y_1 <= 0` (source: sweep_422; source='j1', subset=('a', 'c', 'd'), residual=1)
- `-x_b - x_c - x_d + y_1 <= 0` (source: sweep_422; source='j1', subset=('b', 'c', 'd'), residual=1)
- `-x_a - x_b + y_1 <= 0` (source: sweep_431; source='j1', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_1 <= 0` (source: sweep_431; source='j1', subset=('a', 'c'), residual=1)
- `-x_a - x_d + y_1 <= 0` (source: sweep_431; source='j1', subset=('a', 'd'), residual=1)
- `-x_b - x_c + y_1 <= 0` (source: sweep_431; source='j1', subset=('b', 'c'), residual=1)
- `-x_b - x_d + y_1 <= 0` (source: sweep_431; source='j1', subset=('b', 'd'), residual=1)
- `-x_c - x_d + y_1 <= 0` (source: sweep_431; source='j1', subset=('c', 'd'), residual=1)
- `-x_a - x_b - x_c + 2 y_1 <= 0` (source: sweep_431; source='j1', subset=('a', 'b', 'c'), residual=2)
- `-x_a - x_b - x_d + 2 y_1 <= 0` (source: sweep_431; source='j1', subset=('a', 'b', 'd'), residual=2)
- `-x_a - x_c - x_d + 2 y_1 <= 0` (source: sweep_431; source='j1', subset=('a', 'c', 'd'), residual=2)
- `-x_b - x_c - x_d + 2 y_1 <= 0` (source: sweep_431; source='j1', subset=('b', 'c', 'd'), residual=2)

#### Notes

- Matched instances: boundary_full, disjoint_3x3, medium_nested_6, medium_overlap_5, nested_j2_in_j1, overlap_1, overlap_2, sweep_422, sweep_431.
- Coverage is computational evidence only; completeness is not claimed.

### Residual family for J2

#### Symbolic statement

x(D) >= (b_2 - |J_2 \ D|) y_2

#### Parameter conditions

- D subset J_2
- b_2 - |J_2 \ D| > 0

#### Derivation certificate

- Source row: x(J_k) >= b_k y_k.
- Let E = J_k \ D and use x(E) <= |E|.
- Then x(D) >= (b_k - |J_k \ D|) y_k.
- Gate 1 passed on the matched concrete instances by exact normalized equality.
- Gate 2 passed for the reported concrete matches on enumerated feasible points.
- Gate 3 passed by the residual derivation certificate.

#### Status

- validity: `proved valid for the documented residual derivation route`
- facetness: `facetness unproved`
- completeness: `complete hull not claimed`

#### Covered computed facets

- `-x_d - x_e + y_2 <= 0` (source: disjoint_3x3; source='j2', subset=('d', 'e'), residual=1)
- `-x_d - x_f + y_2 <= 0` (source: disjoint_3x3; source='j2', subset=('d', 'f'), residual=1)
- `-x_e - x_f + y_2 <= 0` (source: disjoint_3x3; source='j2', subset=('e', 'f'), residual=1)
- `-x_c - x_d + y_2 <= 0` (source: overlap_1; source='j2', subset=('c', 'd'), residual=1)
- `-x_c - x_e + y_2 <= 0` (source: overlap_1; source='j2', subset=('c', 'e'), residual=1)
- `-x_d - x_e + y_2 <= 0` (source: overlap_1; source='j2', subset=('d', 'e'), residual=1)
- `-x_c - x_d + y_2 <= 0` (source: overlap_2; source='j2', subset=('c', 'd'), residual=1)
- `-x_c - x_e + y_2 <= 0` (source: overlap_2; source='j2', subset=('c', 'e'), residual=1)
- `-x_d - x_e + y_2 <= 0` (source: overlap_2; source='j2', subset=('d', 'e'), residual=1)
- `-x_a - x_b + y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('a', 'c'), residual=1)
- `-x_a - x_d + y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('a', 'd'), residual=1)
- `-x_b - x_c + y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('b', 'c'), residual=1)
- `-x_b - x_d + y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('b', 'd'), residual=1)
- `-x_c - x_d + y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('c', 'd'), residual=1)
- `-x_a - x_b - x_c + 2 y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('a', 'b', 'c'), residual=2)
- `-x_a - x_b - x_d + 2 y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('a', 'b', 'd'), residual=2)
- `-x_a - x_c - x_d + 2 y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('a', 'c', 'd'), residual=2)
- `-x_b - x_c - x_d + 2 y_2 <= 0` (source: nested_j1_in_j2; source='j2', subset=('b', 'c', 'd'), residual=2)
- `-x_a - x_b + y_2 <= 0` (source: identical; source='j2', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_2 <= 0` (source: identical; source='j2', subset=('a', 'c'), residual=1)
- `-x_b - x_c + y_2 <= 0` (source: identical; source='j2', subset=('b', 'c'), residual=1)
- `-x_c - x_d + y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('c', 'd'), residual=1)
- `-x_c - x_e + y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('c', 'e'), residual=1)
- `-x_c - x_f + y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('c', 'f'), residual=1)
- `-x_d - x_e + y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('d', 'e'), residual=1)
- `-x_d - x_f + y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('d', 'f'), residual=1)
- `-x_e - x_f + y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('e', 'f'), residual=1)
- `-x_c - x_d - x_e + 2 y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('c', 'd', 'e'), residual=2)
- `-x_c - x_d - x_f + 2 y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('c', 'd', 'f'), residual=2)
- `-x_c - x_e - x_f + 2 y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('c', 'e', 'f'), residual=2)
- `-x_d - x_e - x_f + 2 y_2 <= 0` (source: medium_overlap_5; source='j2', subset=('d', 'e', 'f'), residual=2)
- `-x_a - x_b + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'b'), residual=1)
- `-x_a - x_c + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'c'), residual=1)
- `-x_a - x_d + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'd'), residual=1)
- `-x_a - x_e + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'e'), residual=1)
- `-x_b - x_c + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('b', 'c'), residual=1)
- `-x_b - x_d + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('b', 'd'), residual=1)
- `-x_b - x_e + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('b', 'e'), residual=1)
- `-x_c - x_d + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('c', 'd'), residual=1)
- `-x_c - x_e + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('c', 'e'), residual=1)
- `-x_d - x_e + y_2 <= 0` (source: medium_identical_5; source='j2', subset=('d', 'e'), residual=1)
- `-x_a - x_b - x_c + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'b', 'c'), residual=2)
- `-x_a - x_b - x_d + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'b', 'd'), residual=2)
- `-x_a - x_b - x_e + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'b', 'e'), residual=2)
- `-x_a - x_c - x_d + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'c', 'd'), residual=2)
- `-x_a - x_c - x_e + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'c', 'e'), residual=2)
- `-x_a - x_d - x_e + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'd', 'e'), residual=2)
- `-x_b - x_c - x_d + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('b', 'c', 'd'), residual=2)
- `-x_b - x_c - x_e + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('b', 'c', 'e'), residual=2)
- `-x_b - x_d - x_e + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('b', 'd', 'e'), residual=2)
- `-x_c - x_d - x_e + 2 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('c', 'd', 'e'), residual=2)
- `-x_a - x_b - x_c - x_d + 3 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'b', 'c', 'd'), residual=3)
- `-x_a - x_b - x_c - x_e + 3 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'b', 'c', 'e'), residual=3)
- `-x_a - x_b - x_d - x_e + 3 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'b', 'd', 'e'), residual=3)
- `-x_a - x_c - x_d - x_e + 3 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('a', 'c', 'd', 'e'), residual=3)
- `-x_b - x_c - x_d - x_e + 3 y_2 <= 0` (source: medium_identical_5; source='j2', subset=('b', 'c', 'd', 'e'), residual=3)
- `-x_a - x_b - x_d + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'd'), residual=1)
- `-x_a - x_b - x_e + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'e'), residual=1)
- `-x_a - x_b - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'f'), residual=1)
- `-x_a - x_c - x_d + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'c', 'd'), residual=1)
- `-x_a - x_c - x_e + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'c', 'e'), residual=1)
- `-x_a - x_c - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'c', 'f'), residual=1)
- `-x_a - x_d - x_e + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'd', 'e'), residual=1)
- `-x_a - x_d - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'd', 'f'), residual=1)
- `-x_a - x_e - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'e', 'f'), residual=1)
- `-x_b - x_c - x_d + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'c', 'd'), residual=1)
- `-x_b - x_c - x_e + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'c', 'e'), residual=1)
- `-x_b - x_c - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'c', 'f'), residual=1)
- `-x_b - x_d - x_e + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'd', 'e'), residual=1)
- `-x_b - x_d - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'd', 'f'), residual=1)
- `-x_b - x_e - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'e', 'f'), residual=1)
- `-x_c - x_d - x_e + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('c', 'd', 'e'), residual=1)
- `-x_c - x_d - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('c', 'd', 'f'), residual=1)
- `-x_c - x_e - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('c', 'e', 'f'), residual=1)
- `-x_d - x_e - x_f + y_2 <= 0` (source: medium_nested_6; source='j2', subset=('d', 'e', 'f'), residual=1)
- `-x_a - x_b - x_c - x_d + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'c', 'd'), residual=2)
- `-x_a - x_b - x_c - x_e + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'c', 'e'), residual=2)
- `-x_a - x_b - x_c - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'c', 'f'), residual=2)
- `-x_a - x_b - x_d - x_e + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'd', 'e'), residual=2)
- `-x_a - x_b - x_d - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'd', 'f'), residual=2)
- `-x_a - x_b - x_e - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'e', 'f'), residual=2)
- `-x_a - x_c - x_d - x_e + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'c', 'd', 'e'), residual=2)
- `-x_a - x_c - x_d - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'c', 'd', 'f'), residual=2)
- `-x_a - x_c - x_e - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'c', 'e', 'f'), residual=2)
- `-x_a - x_d - x_e - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'd', 'e', 'f'), residual=2)
- `-x_b - x_c - x_d - x_e + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'c', 'd', 'e'), residual=2)
- `-x_b - x_c - x_d - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'c', 'd', 'f'), residual=2)
- `-x_b - x_c - x_e - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'c', 'e', 'f'), residual=2)
- `-x_b - x_d - x_e - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'd', 'e', 'f'), residual=2)
- `-x_c - x_d - x_e - x_f + 2 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('c', 'd', 'e', 'f'), residual=2)
- `-x_a - x_b - x_c - x_d - x_e + 3 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'c', 'd', 'e'), residual=3)
- `-x_a - x_b - x_c - x_d - x_f + 3 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'c', 'd', 'f'), residual=3)
- `-x_a - x_b - x_c - x_e - x_f + 3 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'c', 'e', 'f'), residual=3)
- `-x_a - x_b - x_d - x_e - x_f + 3 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'b', 'd', 'e', 'f'), residual=3)
- `-x_a - x_c - x_d - x_e - x_f + 3 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('a', 'c', 'd', 'e', 'f'), residual=3)
- `-x_b - x_c - x_d - x_e - x_f + 3 y_2 <= 0` (source: medium_nested_6; source='j2', subset=('b', 'c', 'd', 'e', 'f'), residual=3)
- `-x_c - x_d + y_2 <= 0` (source: sweep_421; source='j2', subset=('c', 'd'), residual=1)
- `-x_c - x_e + y_2 <= 0` (source: sweep_421; source='j2', subset=('c', 'e'), residual=1)
- `-x_d - x_e + y_2 <= 0` (source: sweep_421; source='j2', subset=('d', 'e'), residual=1)
- `-x_b - x_c - x_d + y_2 <= 0` (source: sweep_422; source='j2', subset=('b', 'c', 'd'), residual=1)
- `-x_b - x_c - x_e + y_2 <= 0` (source: sweep_422; source='j2', subset=('b', 'c', 'e'), residual=1)
- `-x_b - x_d - x_e + y_2 <= 0` (source: sweep_422; source='j2', subset=('b', 'd', 'e'), residual=1)
- `-x_c - x_d - x_e + y_2 <= 0` (source: sweep_422; source='j2', subset=('c', 'd', 'e'), residual=1)

#### Notes

- Matched instances: disjoint_3x3, identical, medium_identical_5, medium_nested_6, medium_overlap_5, nested_j1_in_j2, overlap_1, overlap_2, sweep_421, sweep_422.
- Coverage is computational evidence only; completeness is not claimed.

## Candidate symbolic inequality families

Families in this section may be useful conjectures or experimentally promising templates, but they are not reported as proved valid. A candidate family must be refined, proved, or invalidated before it can be used as a final mathematical conclusion.

### candidate_overlap_2_x[2,2,0]|y[1,1]|rhs=0

#### Candidate statement

x_a + x_b + x_c + x_d >= -1 y_1 + -1 y_2

#### Gate status

- candidate status: `awaiting c-MIR derivation`
- exact matching: `not globally validated`
- finite validity: `unchecked beyond local concrete evidence`
- derivation: `missing`

#### Why this is not reported as derived

Finite-validity and exact-matching evidence may exist locally, but a symbolic derivation certificate is still missing.

#### Evidence

- -x_a - x_b - x_c - x_d + y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_b - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_a - x_b - x_c + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_d + y_1 + y_2 <= 0
- -x_a - x_b - x_c + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d + 2 y_1 + y_2 <= 0
- -x_b - x_c - x_d + y_1 + y_2 <= 0
- -x_a - x_b - x_c + y_1 + y_2 <= 0
- -x_b - x_c - x_d + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d + y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0
- -x_b - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0
- -x_b - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_b - x_c - x_d - x_f + y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_f + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_d - x_e + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_c - x_d - x_e + 2 y_1 + 2 y_2 <= 0
- -x_b - x_c - x_d - x_e + y_1 + 2 y_2 <= 0
- -x_a - x_c - x_d - x_e + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_c - x_e + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_c + y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d - x_e + 2 y_1 + y_2 <= 0
- -x_b - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_a - x_b - x_d - x_e + y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_f + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d - x_f + 2 y_1 + y_2 <= 0
- -x_b - x_c - x_d - x_f + y_1 + y_2 <= 0
- -x_a - x_b - x_d - x_f + y_1 + y_2 <= 0
- -x_a - x_c - x_e - x_f + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_e - x_f + 2 y_1 + y_2 <= 0
- -x_b - x_c - x_e - x_f + y_1 + y_2 <= 0
- -x_a - x_b - x_e - x_f + y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_c - x_d - x_e - x_f + 2 y_1 + 2 y_2 <= 0
- -x_b - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_d - x_e - x_f + y_1 + 2 y_2 <= 0
- -x_a - x_b - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d + y_1 + y_2 <= 0
- -x_b - x_c - x_d - x_e + y_1 + y_2 <= 0
- -x_a - x_b - x_c - x_d - x_e - x_f + 2 y_1 + y_2 <= 0
- -x_a - x_c - x_d - x_e - x_f + y_1 + y_2 <= 0
- -x_a - x_b - x_d - x_e - x_f + y_1 + y_2 <= 0

#### Next actions

- Retry coefficient tightening on overlap/nested supports.
- Retry aggregation+c-MIR using residual derived rows.
- Search for a mixed-MIR base form with explicit tau/gamma data.

#### Notes

- This is a local candidate inferred from an uncovered concrete facet.
- The family-compression pass merged candidates only when their missing-proof status and next actions agreed.

## Invalidated candidate families

Families in this section were rejected by finite feasible-point checking or by failed exact-instantiation checks.
Invalidated families should be used to refine the next candidate family proposal.

No invalidated candidate family was reported.

## Coverage of computed facets

This section records computational evidence showing which concrete facets are explained by the symbolic families above.
Coverage must be based on exact instantiation and normalization, not on visual similarity.
It is not a proof of completeness.

| family | covered facets | evidence sources | notes |
| --- | ---: | --- | --- |
| residual_j1 | 44 | boundary_full, disjoint_3x3, medium_nested_6, medium_overlap_5, nested_j2_in_j1, overlap_1, overlap_2, sweep_422, sweep_431 | valid_on_points_and_matches_facets |
| residual_j2 | 104 | disjoint_3x3, identical, medium_identical_5, medium_nested_6, medium_overlap_5, nested_j1_in_j2, overlap_1, overlap_2, sweep_421, sweep_422 | valid_on_points_and_matches_facets |


## Derivation attempts for not-yet-covered facets

The following derivation attempts record how computed facets were tested against residual, coefficient-tightening, aggregation, c-MIR, mixed-MIR, or related derivation patterns.

### Target facet: `-x_a - x_b - x_c - x_d + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- overlap_2:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `overlap_2`
  - notes: J1=['a', 'b', 'c', 'd']
- overlap_2:activation_j2
  - symbolic: x(J_2) >= 2 y_2
  - concrete: `overlap_2`
  - notes: J2=['c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_overlap_2_x[2,2,0]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- overlap_2:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `overlap_2`
  - notes: J1=['a', 'b', 'c', 'd']
- overlap_2:activation_j2
  - symbolic: x(J_2) >= 2 y_2
  - concrete: `overlap_2`
  - notes: J2=['c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_overlap_2_x[1,2,1]|y[1,1]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- overlap_2:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `overlap_2`
  - notes: J1=['a', 'b', 'c', 'd']
- overlap_2:activation_j2
  - symbolic: x(J_2) >= 2 y_2
  - concrete: `overlap_2`
  - notes: J2=['c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_overlap_2_x[1,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- nested_j1_in_j2:activation_j1
  - symbolic: x(J_1) >= 1 y_1
  - concrete: `nested_j1_in_j2`
  - notes: J1=['a', 'b']
- nested_j1_in_j2:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `nested_j1_in_j2`
  - notes: J2=['a', 'b', 'c', 'd']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_nested_j1_in_j2_x[0,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- nested_j1_in_j2:activation_j1
  - symbolic: x(J_1) >= 1 y_1
  - concrete: `nested_j1_in_j2`
  - notes: J1=['a', 'b']
- nested_j1_in_j2:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `nested_j1_in_j2`
  - notes: J2=['a', 'b', 'c', 'd']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_nested_j1_in_j2_x[0,2,2]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_d + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_d >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- nested_j1_in_j2:activation_j1
  - symbolic: x(J_1) >= 1 y_1
  - concrete: `nested_j1_in_j2`
  - notes: J1=['a', 'b']
- nested_j1_in_j2:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `nested_j1_in_j2`
  - notes: J2=['a', 'b', 'c', 'd']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_nested_j1_in_j2_x[0,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- nested_j2_in_j1:activation_j1
  - symbolic: x(J_1) >= 3 y_1
  - concrete: `nested_j2_in_j1`
  - notes: J1=['a', 'b', 'c', 'd']
- nested_j2_in_j1:activation_j2
  - symbolic: x(J_2) >= 1 y_2
  - concrete: `nested_j2_in_j1`
  - notes: J2=['b', 'c']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_nested_j2_in_j1_x[1,2,0]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d + 2 y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d >= -2 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- nested_j2_in_j1:activation_j1
  - symbolic: x(J_1) >= 3 y_1
  - concrete: `nested_j2_in_j1`
  - notes: J1=['a', 'b', 'c', 'd']
- nested_j2_in_j1:activation_j2
  - symbolic: x(J_2) >= 1 y_2
  - concrete: `nested_j2_in_j1`
  - notes: J2=['b', 'c']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_nested_j2_in_j1_x[2,2,0]|y[2,1]|rhs=0

### Target facet: `-x_b - x_c - x_d + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- nested_j2_in_j1:activation_j1
  - symbolic: x(J_1) >= 3 y_1
  - concrete: `nested_j2_in_j1`
  - notes: J1=['a', 'b', 'c', 'd']
- nested_j2_in_j1:activation_j2
  - symbolic: x(J_2) >= 1 y_2
  - concrete: `nested_j2_in_j1`
  - notes: J2=['b', 'c']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_nested_j2_in_j1_x[1,2,0]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- identical:activation_j1
  - symbolic: x(J_1) >= 1 y_1
  - concrete: `identical`
  - notes: J1=['a', 'b', 'c']
- identical:activation_j2
  - symbolic: x(J_2) >= 2 y_2
  - concrete: `identical`
  - notes: J2=['a', 'b', 'c']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_identical_x[0,3,0]|y[1,1]|rhs=0

### Target facet: `-x_b - x_c - x_d + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- boundary_full:activation_j1
  - symbolic: x(J_1) >= 3 y_1
  - concrete: `boundary_full`
  - notes: J1=['a', 'b', 'c']
- boundary_full:activation_j2
  - symbolic: x(J_2) >= 1 y_2
  - concrete: `boundary_full`
  - notes: J2=['b', 'c', 'd']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_boundary_full_x[0,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_overlap_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_overlap_5`
  - notes: J1=['a', 'b', 'c', 'd']
- medium_overlap_5:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `medium_overlap_5`
  - notes: J2=['c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_overlap_5_x[2,2,0]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_e + x_f >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_overlap_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_overlap_5`
  - notes: J1=['a', 'b', 'c', 'd']
- medium_overlap_5:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `medium_overlap_5`
  - notes: J2=['c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_overlap_5_x[1,2,2]|y[1,2]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_e + x_f >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_overlap_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_overlap_5`
  - notes: J1=['a', 'b', 'c', 'd']
- medium_overlap_5:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `medium_overlap_5`
  - notes: J2=['c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_overlap_5_x[1,2,2]|y[1,2]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_overlap_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_overlap_5`
  - notes: J1=['a', 'b', 'c', 'd']
- medium_overlap_5:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `medium_overlap_5`
  - notes: J2=['c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_overlap_5_x[1,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_overlap_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_overlap_5`
  - notes: J1=['a', 'b', 'c', 'd']
- medium_overlap_5:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `medium_overlap_5`
  - notes: J2=['c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_overlap_5_x[1,2,1]|y[1,1]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_overlap_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_overlap_5`
  - notes: J1=['a', 'b', 'c', 'd']
- medium_overlap_5:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `medium_overlap_5`
  - notes: J2=['c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_overlap_5_x[1,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_overlap_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_overlap_5`
  - notes: J1=['a', 'b', 'c', 'd']
- medium_overlap_5:activation_j2
  - symbolic: x(J_2) >= 3 y_2
  - concrete: `medium_overlap_5`
  - notes: J2=['c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_overlap_5_x[1,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_identical_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_identical_5`
  - notes: J1=['a', 'b', 'c', 'd', 'e']
- medium_identical_5:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_identical_5`
  - notes: J2=['a', 'b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_identical_5_x[0,4,0]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_d - x_e + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_d + x_e >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_identical_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_identical_5`
  - notes: J1=['a', 'b', 'c', 'd', 'e']
- medium_identical_5:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_identical_5`
  - notes: J2=['a', 'b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_identical_5_x[0,4,0]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d - x_e + 2 y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d + x_e >= -2 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_identical_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_identical_5`
  - notes: J1=['a', 'b', 'c', 'd', 'e']
- medium_identical_5:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_identical_5`
  - notes: J2=['a', 'b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_identical_5_x[0,5,0]|y[2,2]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_e + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_e >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_identical_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_identical_5`
  - notes: J1=['a', 'b', 'c', 'd', 'e']
- medium_identical_5:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_identical_5`
  - notes: J2=['a', 'b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_identical_5_x[0,4,0]|y[1,2]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_e + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_e >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_identical_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_identical_5`
  - notes: J1=['a', 'b', 'c', 'd', 'e']
- medium_identical_5:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_identical_5`
  - notes: J2=['a', 'b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_identical_5_x[0,4,0]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_e + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_e >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_identical_5:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_identical_5`
  - notes: J1=['a', 'b', 'c', 'd', 'e']
- medium_identical_5:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_identical_5`
  - notes: J2=['a', 'b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_identical_5_x[0,4,0]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_c + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,3,0]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d - x_e + 2 y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d + x_e >= -2 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,3,2]|y[2,1]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d - x_f + 2 y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d + x_f >= -2 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,3,2]|y[2,1]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_d - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_d + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_e - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_e + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_e - x_f + 2 y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_e + x_f >= -2 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,3,2]|y[2,1]|rhs=0

### Target facet: `-x_b - x_c - x_e - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_e + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_e - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_e + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_e + x_f >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,3]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d - x_e - x_f + 2 y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d + x_e + x_f >= -2 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,3,3]|y[2,2]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_e + x_f >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,3]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_d + x_e + x_f >= -1 y_1 + -2 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- medium_nested_6:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `medium_nested_6`
  - notes: J1=['a', 'b', 'c']
- medium_nested_6:activation_j2
  - symbolic: x(J_2) >= 4 y_2
  - concrete: `medium_nested_6`
  - notes: J2=['a', 'b', 'c', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_medium_nested_6_x[0,2,3]|y[1,2]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- sweep_421:activation_j1
  - symbolic: x(J_1) >= 1 y_1
  - concrete: `sweep_421`
  - notes: J1=['a', 'b', 'c', 'd']
- sweep_421:activation_j2
  - symbolic: x(J_2) >= 2 y_2
  - concrete: `sweep_421`
  - notes: J2=['c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_sweep_421_x[2,2,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- sweep_422:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `sweep_422`
  - notes: J1=['a', 'b', 'c', 'd']
- sweep_422:activation_j2
  - symbolic: x(J_2) >= 2 y_2
  - concrete: `sweep_422`
  - notes: J2=['b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_sweep_422_x[1,3,0]|y[1,1]|rhs=0

### Target facet: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_b + x_c + x_d + x_e >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- sweep_422:activation_j1
  - symbolic: x(J_1) >= 2 y_1
  - concrete: `sweep_422`
  - notes: J1=['a', 'b', 'c', 'd']
- sweep_422:activation_j2
  - symbolic: x(J_2) >= 2 y_2
  - concrete: `sweep_422`
  - notes: J2=['b', 'c', 'd', 'e']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_sweep_422_x[0,3,1]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_c - x_d - x_e - x_f + 2 y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_c + x_d + x_e + x_f >= -2 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- sweep_431:activation_j1
  - symbolic: x(J_1) >= 3 y_1
  - concrete: `sweep_431`
  - notes: J1=['a', 'b', 'c', 'd']
- sweep_431:activation_j2
  - symbolic: x(J_2) >= 1 y_2
  - concrete: `sweep_431`
  - notes: J2=['a', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_sweep_431_x[2,2,2]|y[2,1]|rhs=0

### Target facet: `-x_a - x_c - x_d - x_e - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_c + x_d + x_e + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- sweep_431:activation_j1
  - symbolic: x(J_1) >= 3 y_1
  - concrete: `sweep_431`
  - notes: J1=['a', 'b', 'c', 'd']
- sweep_431:activation_j2
  - symbolic: x(J_2) >= 1 y_2
  - concrete: `sweep_431`
  - notes: J2=['a', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_sweep_431_x[1,2,2]|y[1,1]|rhs=0

### Target facet: `-x_a - x_b - x_d - x_e - x_f + y_1 + y_2 <= 0`

- status: `candidate`
- symbolic family: x_a + x_b + x_d + x_e + x_f >= -1 y_1 + -1 y_2
- equality check: not passed
- failure reason: Target contains nonzero coefficients outside the selected source row and activation variable.

#### Source constraints

- sweep_431:activation_j1
  - symbolic: x(J_1) >= 3 y_1
  - concrete: `sweep_431`
  - notes: J1=['a', 'b', 'c', 'd']
- sweep_431:activation_j2
  - symbolic: x(J_2) >= 1 y_2
  - concrete: `sweep_431`
  - notes: J2=['a', 'd', 'e', 'f']

#### Derivation steps

- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- residual: Target contains nonzero coefficients outside the selected source row and activation variable.
  - status: `failed`
  - notes: Target contains nonzero coefficients outside the selected source row and activation variable.
- coefficient_tightening: Identify source rows and target support.
  - status: `attempted`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- coefficient_tightening: Try upper-bound substitution, lower-bound substitution, complementation, and coefficient strengthening.
  - status: `needs_problem_specific_derivation`
  - notes: Generic coefficient tightening requires model-specific choices of subsets, bounds, and coefficients. A problem adapter should try the documented coefficient-tightening pattern and record the pre-tightening and post-tightening inequalities.
- source_identification: Collected source rows whose supports overlap the target facet.
  - status: `attempted`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- aggregation_cmir: Choose nonnegative multipliers, aggregate rows, then apply c-MIR.
  - status: `needs_problem_specific_derivation`
  - notes: Generic aggregation+c-MIR requires choosing multipliers and identifying the integer and bounded parts of the aggregate. This must be provided by a problem-specific adapter or a more specialized pattern handler.
- mixed_mir: Try to put source rows into valid mixed-MIR base-inequality form.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mixed_mir: If base rows are found, compute tau, gamma, gamma ordering, and common bar_f.
  - status: `needs_problem_specific_derivation`
  - notes: Mixed MIR is not ordinary aggregation. The adapter must provide base inequalities f^i(x)+B g^i(x)>=pi_i, prove f^i>=0 and g^i integral, compute tau_i and gamma_i, identify a common dominating bar_f, and simplify the mixed-MIR inequality.
- mir_after_mir: Search for previously derived valid inequalities that can serve as new source rows.
  - status: `needs_problem_specific_derivation`
  - notes: MIR-after-MIR requires one or more previously derived valid inequalities to be used as new source rows. The generic attemptor does not invent these rows automatically.

#### Notes

- Candidate family proposed: candidate_sweep_431_x[1,2,2]|y[1,1]|rhs=0


## Unresolved computed facets

The following computed facets remain unresolved after the derivation attempts above.

- inequality: `-x_a - x_b - x_c - x_d + y_1 + y_2 <= 0`
  - source: overlap_2
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: overlap_2
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: overlap_2
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c + y_1 + y_2 <= 0`
  - source: nested_j1_in_j2
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d + y_1 + 2 y_2 <= 0`
  - source: nested_j1_in_j2
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_d + y_1 + y_2 <= 0`
  - source: nested_j1_in_j2
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c + y_1 + y_2 <= 0`
  - source: nested_j2_in_j1
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d + 2 y_1 + y_2 <= 0`
  - source: nested_j2_in_j1
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d + y_1 + y_2 <= 0`
  - source: nested_j2_in_j1
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c + y_1 + y_2 <= 0`
  - source: identical
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d + y_1 + y_2 <= 0`
  - source: boundary_full
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d + y_1 + y_2 <= 0`
  - source: medium_overlap_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`
  - source: medium_overlap_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`
  - source: medium_overlap_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: medium_overlap_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: medium_overlap_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_f + y_1 + y_2 <= 0`
  - source: medium_overlap_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_f + y_1 + y_2 <= 0`
  - source: medium_overlap_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d + y_1 + 2 y_2 <= 0`
  - source: medium_identical_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_d - x_e + y_1 + 2 y_2 <= 0`
  - source: medium_identical_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d - x_e + 2 y_1 + 2 y_2 <= 0`
  - source: medium_identical_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_e + y_1 + 2 y_2 <= 0`
  - source: medium_identical_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_e + y_1 + 2 y_2 <= 0`
  - source: medium_identical_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_e + y_1 + 2 y_2 <= 0`
  - source: medium_identical_5
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d - x_e + 2 y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_d - x_e + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_f + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d - x_f + 2 y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_f + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_d - x_f + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_e - x_f + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_e - x_f + 2 y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_e - x_f + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_e - x_f + y_1 + y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d - x_e - x_f + 2 y_1 + 2 y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_d - x_e - x_f + y_1 + 2 y_2 <= 0`
  - source: medium_nested_6
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: sweep_421
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d + y_1 + y_2 <= 0`
  - source: sweep_422
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_b - x_c - x_d - x_e + y_1 + y_2 <= 0`
  - source: sweep_422
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_c - x_d - x_e - x_f + 2 y_1 + y_2 <= 0`
  - source: sweep_431
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_c - x_d - x_e - x_f + y_1 + y_2 <= 0`
  - source: sweep_431
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.
- inequality: `-x_a - x_b - x_d - x_e - x_f + y_1 + y_2 <= 0`
  - source: sweep_431
  - reason: Target contains nonzero coefficients outside the selected source row and activation variable.

## Proof obligations

1. Prove validity of the residual families for all admissible parameters as symbolic statements, not just on tested instances.
2. Characterize when each residual family instance is facet-defining.
3. For each candidate interaction family, either derive it using coefficient tightening / aggregation+c-MIR / mixed MIR / MIR-after-MIR or invalidate/refine it.
4. Surface backend equations explicitly if they occur in future runs instead of relying on the current backend limitation note.
5. Prove reverse inclusion before claiming a complete convex-hull description.
6. Resolve or certify blockers for the remaining 47 unresolved nontrivial facets.
7. Complete Gate 1–3 validation for the remaining 1 candidate families.

## Conclusion

The current output is a family-discovery report. It separates derived families, candidate families, invalidated families, and unresolved computed facets. It does not by itself constitute a complete convex-hull description.

## Appendix: computational evidence

The appendix may contain raw computational evidence. It is not the main mathematical output.

## Computational setup

The study enumerates feasible 0-1 points and computes hull inequalities with pycddlib.

| instance | stage | feasible points | inequalities | nontrivial facets |
| --- | --- | ---: | ---: | ---: |
| sanity_disjoint_2 | sanity | 49 | 14 | 0 |
| sanity_overlap_1 | sanity | 25 | 12 | 0 |
| disjoint_3x3 | structured | 144 | 24 | 6 |
| overlap_1 | structured | 74 | 22 | 6 |
| overlap_2 | structured | 84 | 26 | 10 |
| nested_j1_in_j2 | structured | 38 | 27 | 13 |
| nested_j2_in_j1 | structured | 38 | 27 | 13 |
| identical | structured | 23 | 15 | 4 |
| boundary_full | structured | 34 | 12 | 4 |
| medium_overlap_5 | medium | 146 | 39 | 21 |
| medium_identical_5 | medium | 70 | 46 | 31 |
| medium_nested_6 | medium | 137 | 78 | 60 |
| sweep_421 | sweep | 94 | 20 | 4 |
| sweep_422 | sweep | 95 | 26 | 10 |
| sweep_431 | sweep | 164 | 31 | 13 |

## Facet-to-family discovery rule

Do not stop after listing instance-level facets.

For every nontrivial facet found in a small instance:

1. Translate the concrete inequality into the original symbolic notation.
2. Identify which original constraint or constraints contribute variables to the facet.
3. Identify which variable bounds are implicitly used.
4. Try to derive the concrete inequality from those source constraints using c-MIR, aggregation, complementation, or upper-bound substitution.
5. After a concrete derivation is found, generalize the same derivation to the original parametric model.
6. State the resulting general valid inequality family.
7. Report which computed facets are covered by this family.
8. Only then include the family in the research report.

## Unmatched facet derivation protocol

A computed facet must not be reported as merely "unmatched" until the assistant has attempted:

1. identify source constraints by support overlap;
2. check whether it is an aggregation of multiple original constraints with coefficient tightening;
3. check whether c-MIR or mixed-integer rounding can produce it;
4. check whether it can be obtained by more than one c-MIR patterns, e.g., mixing after residual.
5. if a concrete derivation is found, generalize the same derivation to the symbolic model;
6. only if all attempts fail, place it in the unresolved section with an explicit failure reason.
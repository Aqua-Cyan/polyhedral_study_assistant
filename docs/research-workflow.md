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
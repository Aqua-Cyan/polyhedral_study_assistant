# Facet-coverage protocol

## Problem this solves

The study adapter recomputes `reports/<problem_id>_state.json` from a fixed classifier every loop round. Families the agent proves during the loop only land in `memory/` and were never reflected in the summary counts (`candidate_records`, `unresolved_records`) the regulator keys on. As a result the regulator's stop condition could never be satisfied even after all facets were theoretically found, and the loop ran until `--rounds` was exhausted.

## The coverage manifest

A persistent manifest records which computed facets are covered by accepted symbolic families.

Shape:

```json
{
  "problem_id": "malp",
  "covered": [
    {
      "inequality": {
        "coefficients": [1, 0, 1],
        "rhs": 1,
        "sense": "<=",
        "support": []
      },
      "family": "accepted_family_name",
      "source": "verification file or derivation certificate id",
      "note": "optional"
    }
  ]
}
```

`apply_coverage` (in `src/psa/coverage.py`) keys a facet by the normalized `(coefficients, rhs, sense)` triple and matches by exact equality — the same standard as `psa.family.match_instantiation_to_facets`. Visual similarity is never counted as coverage, consistent with CLAUDE.md Gate 1.

## Loop integration

`scripts/psa_loop.py` runs, per round:

1. The study adapter writes a fresh state from the fixed classifier.
2. `apply_coverage_to_state_file` overlays the persistent manifest:
   - covered facets move from `candidate_facets`/`unresolved_facets` into `covered_facets` and are relabeled `derived`;
   - `summary.covered_records`/`candidate_records`/`unresolved_records` and `stop_status` are recomputed;
   - `proof_obligations` are recomputed.
3. The regulator reads the updated state.

The manifest lives under `memory/` and the study adapter does not write or delete it, so coverage is persistent across rounds. Even though the adapter re-injects interaction facets into `candidate` each round, the overlay prunes them again, so the two counters decrease monotonically as the agent accepts more families.

## What the agent must do

After a family is accepted (verifier verdict `accept_for_implementation` and/or a derivation certificate exists), the agent records each facet that the family covers by exact instantiation and normalization in `memory/facets/<problem_id>/coverage.json`.

## Rules

- Record only accepted/proved families, never pure candidate or `invalid`/`needs_revision` families.
- The `inequality` field must be the normalized cddlib facet inequality matched by exact equality.
- Append or merge; do not delete prior covered entries between rounds.
- If a family is later invalidated, remove its covered entries in the same edit.

## Design boundary

This is a generic framework mechanism. It does not implement any problem-specific family itself; problem-specific instantiation, matching, and derivation remain the agent's job during the loop. The framework only guarantees that once the agent records coverage, the loop can converge.

\goal
You are continuing the `malp` integer-hull discovery research loop.

Do not stop after producing an intermediate report.
Do not ask the user whether to continue merely because one stage is complete.

Stop only if one of the following is true:

1. all computed nontrivial facets in the current tested scope are covered by derived/proved symbolic families;
2. every remaining facet has a documented failure chain and a concrete blocker;
3. a real software or mathematical blocker prevents progress, and you report the blocker, completed work, and smallest next action.

If there are candidate families, unresolved facets, missing derivation certificates, failed exact matches, or missing finite validity checks, the task is not complete.
\endgoal

# Context files to read first

- `reports/malp_state.json`
- `tasks/TASK_POOL.json`
- `reports/malp_report.md`
- `memory/facets/malp/facet_signatures.json`
- `memory/family/malp/family_memory.json`
- `docs/research-workflow.md`
- `docs/reporting-standard.md`
- `docs/facet-analysis.md` if present
- `docs/cmir_patterns/` if present

# Regulator decision

- decision: `RUN_FAMILY_GUESSER`
- reason: Research is not complete: candidate_records=728, unresolved_records=0, signature_count=198. Selected concrete task `malp-family-compression-0001` of type `family_compression`.
- next agent role: `FamilyGuesser`
- success criterion: Replace multiple local candidate families with a smaller number of general parameterized candidate families, or explain why compression failed.

# Selected task

- task id: `malp-family-compression-0001`
- task type: `family_compression`
- priority: `1`
- assigned agent: `FamilyGuesser`

## Required actions

- cluster candidate facets by support and coefficient pattern
- search for a common parameterized family
- express family using D, J1\D, J2\D, intersections, and threshold residuals
- instantiate proposed family on all tested instances
- send to Verifier for exact matching and finite validity

# Your role: FamilyGuesser

You are not proving the family yet.
You are not allowed to mark a family as derived or proved.

Your job is to inspect the candidate facet clusters and propose a small number of more general symbolic families that may subsume many local candidates.

Focus especially on:

- repeated support patterns;
- repeated coefficient patterns;
- interaction facets involving multiple activation variables;
- possible subset-parameterized forms using `D`, complements, intersections, and set differences;
- residual expressions such as `b - |J \ D|`; 
- MIR-over-MIR or derived-row reuse routes.

# Output requirement

Create or overwrite this JSON file:

`memory/family/malp/guesses/malp-family-compression-0001.json`

The JSON must have this schema:

```json
{
  "problem_id": "...",
  "source_task_id": "...",
  "agent": "FamilyGuesser",
  "status": "proposed",
  "family_id": "short_unique_name",
  "family_name": "human readable name",
  "symbolic_statement_latex": "...",
  "normalized_template": "...",
  "parameters": ["D", "..."],
  "parameter_conditions": ["..."],
  "subsumed_signatures": ["..."],
  "evidence_facets": [
    {
      "instance": "...",
      "facet": "...",
      "parameter_values": {"D": "..."}
    }
  ],
  "expected_derivation_route": [
    "residual",
    "support relaxation",
    "mixed MIR or MIR-over-MIR"
  ],
  "validation_plan": [
    "instantiate on tested instances",
    "exact normalized matching",
    "finite validity check",
    "derivation certificate check"
  ],
  "known_risks": ["..."],
  "notes": "..."
}
```

# Rules

1. Prefer one general parameterized family over many local families.
2. Do not hard-code one tested instance as a family.
3. Do not claim validity merely from computational evidence.
4. Do not add the family to derived families.
5. Do not modify source code unless necessary.
6. If the current clusters are too heterogeneous, propose several candidate families, but keep the number small.
7. If no useful generalization is found, write a guess JSON with status `no_good_guess` and explain why.

# Expected final response

Report:

1. which guess file you wrote;
2. which signatures or facets it tries to subsume;
3. why the proposed family is more general than the local candidates;
4. what the Verifier should check next.

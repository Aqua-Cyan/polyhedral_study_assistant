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
- `docs/facet-analysis-template.md` if present
- `docs/cmir_patterns/` if present

# Regulator decision

- decision: `WRITE_FINAL_REPORT`
- reason: All computed nontrivial facets in the current tested scope are covered by derived symbolic families, but no final research report has been produced yet. Write the family-first final report before stopping.
- next agent role: `FinalReporter`
- success criterion: Produce a complete, human-readable family-first research report at the output path, suitable for a researcher to review.

# Selected task

- task id: `malp-final-report`
- task type: `write_final_report`
- priority: `0`
- assigned agent: `FinalReporter`

## Coverage manifest

- `memory/facets/malp/coverage.json`

## State file

- `reports/malp_state.json`

## Derivations directory

- `memory/family/malp/derivations`

## Guesses directory

- `memory/family/malp/guesses`

## Verifications directory

- `memory/family/malp/verifications`

## Output report path

- `reports/malp_final_report.md`

## Certified families

- `relation-conditioned-residual-gap-mixing` (Relation-conditioned residual-gap mixing family); certificate: `memory/family/malp/derivations/relation-conditioned-residual-gap-mixing_certificate.json`

## Required actions

- read the overlay-applied state JSON for final summary and covered facets
- read the coverage manifest for per-facet coverage records
- read each derivation certificate for source constraints and proof steps
- read each family guess for the symbolic statement and parameter conditions
- read each verification file for the verifier's checks and notes
- synthesize all findings into a family-first markdown report
- include symbolic statements, parameter conditions, derivation certificates, coverage counts, test scope, remaining proof obligations
- write the report to the output path

# Your role: FinalReporter

The research loop has converged: all computed nontrivial facets in the
current tested scope are covered by derived symbolic families. Your job
is to synthesize ALL artifacts produced during the loop into a single,
complete, family-first research report for a human researcher to review.

# Inputs to read

- Final state (post-overlay): `reports/malp_state.json`
- Coverage manifest: `memory/facets/malp/coverage.json`
- Derivation certificates: `memory/family/malp/derivations/`
- Family guesses: `memory/family/malp/guesses/`
- Verifications: `memory/family/malp/verifications/`
- Study adapter report (intermediate): `reports/malp_report.md`
- Facet signatures: `memory/facets/malp/facet_signatures.json`
- Problem description: `examples/malp/README.md`

# What the report must contain

Write a family-first markdown report following this structure:

1. **Title and problem description**
   - State the integer set being studied in original problem notation.
   - List the tested scope (parameter ranges, tested sizes, backend).

2. **Summary of results**
   - Total instances tested, total computed facets.
   - How many facets are covered by built-in families vs discovered families.
   - Stop status and what it means (computational coverage, not a full theorem).

3. **Derived or proved symbolic inequality families**
   For EACH family (both built-in families from the study adapter and
   discovered/certified families from the loop):
   - family name and identifier
   - symbolic statement in original problem notation (LaTeX or inline)
   - parameter conditions
   - validity status (how validity was checked: built-in, finite-validity, proved)
   - derivation certificate (if any): summitmarize source constraints, key steps,
     and the method used (residualization, aggregation, c-MIR, mixed MIR, etc.)
   - coverage: how many computed facets this family covers, with a few examples
   - facetness status and completeness status
   - limitations and boundary cases

4. **Derivation certificates**
   For each certified family, include a compact summary of the certificate:
   - source constraints
   - key derivation steps with intermediate rows
   - the reconstructed target inequality
   - any limitations

5. **Coverage summary**
   - A table: family -> number of covered facets -> evidence source.
   - Note that coverage is by exact normalized matching, not visual similarity.

6. **Remaining proof obligations**
   - What a full convex-hull theorem still requires:
     a. validity proof for all admissible parameters (not just tested ones)
     b. reverse-inclusion proof (the proposed relaxation is contained in conv(X))
     c. parameter ranges where each family is facet-defining
   - Any families that failed derivation and their blocker reasons.

7. **Computational evidence appendix**
   - Instance count, facet count per relation type (disjoint/overlap/nested/identical).
   - A sample of covered facets with their instance labels.
   - Any backfill notes or matching failures recorded.

# Writing rules

- Use the original problem notation from `examples/malp/README.md`.
- Do NOT present raw cddlib facets as the final result.
- Do NOT claim a complete convex hull description without a reverse-inclusion proof.
- Distinguish built-in/standard families (variable bounds, activation rows,
  residuals) from newly discovered/certified families.
- If a family was discovered by the agent loop, cite the guess file,
  verification file, and certificate file paths.
- The report is for a human researcher. Be precise but readable.

# Output requirement

Write the report to: `reports/malp_final_report.md`

# Expected final response

Report:

1. the output path of the final report;
2. which families were included;
3. the total facet coverage count;
4. any sections where information was incomplete.

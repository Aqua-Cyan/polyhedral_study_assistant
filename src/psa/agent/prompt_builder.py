from __future__ import annotations

from pathlib import Path
from typing import Any

from psa.agent.regulator import RegulatorDecision
from psa.agent.state import ResearchState

_NL = chr(10)


def build_next_claude_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    next_agent = decision.next_agent or "ClaudeCode"

    if next_agent == "FamilyGuesser":
        return _build_family_guesser_prompt(
            project_root=project_root, state=state, decision=decision
        )

    if next_agent == "Verifier":
        return _build_verifier_prompt(
            project_root=project_root, state=state, decision=decision
        )

    if next_agent == "DerivationProver":
        return _build_derivation_prover_prompt(
            project_root=project_root, state=state, decision=decision
        )

    if next_agent == "CoverageBackfiller":
        return _build_backfill_coverage_prompt(
            project_root=project_root, state=state, decision=decision
        )

    if next_agent == "FinalReporter":
        return _build_final_report_prompt(
            project_root=project_root, state=state, decision=decision
        )

    return _build_generic_executor_prompt(
        project_root=project_root, state=state, decision=decision
    )


def _goal_block(problem_id: str) -> list[str]:
    return [
        "\\goal",
        f"You are continuing the `{problem_id}` integer-hull discovery research loop.",
        "",
        "Do not stop after producing an intermediate report.",
        "Do not ask the user whether to continue merely because one stage is complete.",
        "",
        "Stop only if one of the following is true:",
        "",
        "1. all computed nontrivial facets in the current tested scope are covered by derived/proved symbolic families;",
        "2. every remaining facet has a documented failure chain and a concrete blocker;",
        "3. a real software or mathematical blocker prevents progress, and you report the blocker, completed work, and smallest next action.",
        "",
        "If there are candidate families, unresolved facets, missing derivation certificates, failed exact matches, or missing finite validity checks, the task is not complete.",
        "\\endgoal",
        "",
    ]


def _context_files(problem_id: str) -> list[str]:
    return [
        "# Context files to read first",
        "",
        f"- `reports/{problem_id}_state.json`",
        "- `tasks/TASK_POOL.json`",
        f"- `reports/{problem_id}_report.md`",
        f"- `memory/facets/{problem_id}/facet_signatures.json`",
        f"- `memory/family/{problem_id}/family_memory.json`",
        "- `docs/research-workflow.md`",
        "- `docs/reporting-standard.md`",
        "- `docs/facet-analysis-template.md` if present",
        "- `docs/cmir_patterns/` if present",
        "",
    ]


def _decision_block(decision: RegulatorDecision) -> list[str]:
    return [
        "# Regulator decision",
        "",
        f"- decision: `{decision.decision}`",
        f"- reason: {decision.reason}",
        f"- next agent role: `{decision.next_agent}`",
        f"- success criterion: {decision.success_criterion}",
        "",
    ]


def _selected_task_block(task: dict[str, Any] | None) -> list[str]:
    if task is None:
        return []

    lines: list[str] = [
        "# Selected task",
        "",
        f"- task id: `{task.get('id')}`",
        f"- task type: `{task.get('type')}`",
        f"- priority: `{task.get('priority')}`",
        f"- assigned agent: `{task.get('assigned_agent')}`",
        "",
    ]

    if "guess_file" in task:
        lines.extend(["## Guess file", "", f"- `{task['guess_file']}`", ""])

    if "verification_file" in task:
        lines.extend(["## Verification file to write", "", f"- `{task['verification_file']}`", ""])

    if "signature" in task:
        lines.extend(["## Facet signature", "", f"`{task['signature']}`", ""])

    if "coverage_manifest" in task:
        lines.extend(["## Coverage manifest", "", f"- `{task['coverage_manifest']}`", ""])

    if "state_file" in task:
        lines.extend(["## State file", "", f"- `{task['state_file']}`", ""])

    if "derivations_dir" in task:
        lines.extend(["## Derivations directory", "", f"- `{task['derivations_dir']}`", ""])

    if "guesses_dir" in task:
        lines.extend(["## Guesses directory", "", f"- `{task['guesses_dir']}`", ""])

    if "verifications_dir" in task:
        lines.extend(["## Verifications directory", "", f"- `{task['verifications_dir']}`", ""])

    if "output_path" in task:
        lines.extend(["## Output report path", "", f"- `{task['output_path']}`", ""])

    if task.get("certified_families"):
        lines.extend(["## Certified families", ""])
        for fam in task["certified_families"]:
            if isinstance(fam, dict):
                lines.append(
                    f"- `{fam.get('family_id')}` ({fam.get('family_name')}); "
                    f"certificate: `{fam.get('certificate_file')}`"
                )
            else:
                lines.append(f"- `{fam}`")
        lines.append("")

    if task.get("pending_families"):
        lines.extend(["## Pending accepted families", ""])
        for fam in task["pending_families"]:
            if isinstance(fam, dict):
                cert = fam.get("certificate_file")
                cert_str = f"; certificate: `{cert}`" if cert else "; NO certificate yet"
                lines.append(
                    f"- `{fam.get('family_id')}` ({fam.get('family_name')}){cert_str}; "
                    f"verification: `{fam.get('verification_file')}`; "
                    f"guess: `{fam.get('guess_file')}`"
                )
            else:
                lines.append(f"- `{fam}`")
        lines.append("")

    if task.get("sample_facets"):
        lines.extend(["## Sample facets", ""])
        for item in task["sample_facets"]:
            text = item.get("text")
            instance = item.get("instance", {}).get("label") or item.get("instance_label")
            derivation_status = item.get("derivation_status")
            lines.append(f"- `{text}` from `{instance}`; derivation_status=`{derivation_status}`")
        lines.append("")

    if task.get("required_actions"):
        lines.extend(["## Required actions", ""])
        for action in task["required_actions"]:
            lines.append(f"- {action}")
        lines.append("")

    return lines


def _coverage_protocol_block(problem_id: str) -> list[str]:
    return [
        "# Facet-coverage bookkeeping",
        "",
        "The regulator's stop condition is driven by `candidate_records` and",
        "`unresolved_records` in `reports/" + problem_id + "_state.json`. These counts",
        "are recomputed from a fixed classifier in the study adapter each round and",
        "do NOT reflect families you proved during the loop. To close the loop you",
        "must record covered facets in a persistent manifest:",
        "",
        f"`memory/facets/{problem_id}/coverage.json`",
        "",
        "This manifest is overlaid onto the state after each study-adapter run, so",
        "covered facets are pruned from candidate/unresolved and the stop counters",
        "can actually reach zero.",
        "",
        "Format:",
        "",
        "```json",
        "{",
        '  "problem_id": "' + problem_id + '",',
        '  "covered": [',
        "    {",
        '      "inequality": {"coefficients": [..exact ints..], "rhs": int, "sense": "<=", "support": [...]},',
        '      "family": "accepted_family_id",',
        '      "source": "verification file or derivation certificate id",',
        '      "note": "optional human note"',
        "    }",
        "  ],",
        '  "backfilled_families": ["accepted_family_id_1", "accepted_family_id_2"]',
        "}",
        "```",
        "",
        "Rules:",
        "",
        "1. Record a facet only after the family is ACCEPTED and has a derivation",
        "   certificate (verifier verdict `accept_for_implementation` plus a certificate",
        "   file in `memory/family/" + problem_id + "/derivations/`).",
        "2. The `inequality` field MUST be the normalized cdd facet inequality, by",
        "   exact coefficient/rhs/sense equality (not visual similarity).",
        "3. Never record a pure `candidate` (no certificate) or an `invalid`/",
        "   `needs_revision` family as covered.",
        "4. Append or merge entries; do NOT delete prior covered entries between",
        "   rounds (the manifest is persistent and only the overlay prunes).",
        "5. Append the family id to `backfilled_families` once you have recorded all",
        "   its covered facets for this scope, so the regulator stops re-requesting it.",
        "6. If a family is later invalidated, remove both its covered entries and its",
        "   `backfilled_families` entry in one edit.",
        "",
    ]


def _build_family_guesser_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    problem_id = state.problem_id
    task = decision.selected_task
    task_id = str(task.get("id", "family-guess")) if task else "family-guess"

    guess_path = f"memory/family/{problem_id}/guesses/{task_id}.json"

    lines: list[str] = []
    lines.extend(_goal_block(problem_id))
    lines.extend(_context_files(problem_id))
    lines.extend(_decision_block(decision))
    lines.extend(_selected_task_block(task))

    lines.extend(
        [
            "# Your role: FamilyGuesser",
            "",
            "You are not proving the family yet.",
            "You are not allowed to mark a family as derived or proved.",
            "",
            "Your job is to inspect the candidate facet clusters and propose a small number of more general symbolic families that may subsume many local candidates.",
            "",
            "Focus especially on:",
            "",
            "- repeated support patterns;",
            "- repeated coefficient patterns;",
            "- interaction facets involving multiple activation variables;",
            "- possible subset-parameterized forms using `D`, complements, intersections, and set differences;",
            "- residual expressions such as `b - |J \\ D|`;",
            "- MIR-over-MIR or derived-row reuse routes.",
            "",
            "# Output requirement",
            "",
            "Create or overwrite this JSON file:",
            "",
            f"`{guess_path}`",
            "",
            "The JSON must have this schema:",
            "",
            "```json",
            "{",
            '  "problem_id": "...",',
            '  "source_task_id": "...",',
            '  "agent": "FamilyGuesser",',
            '  "status": "proposed",',
            '  "family_id": "short_unique_name",',
            '  "family_name": "human readable name",',
            '  "symbolic_statement_latex": "...",',
            '  "normalized_template": "...",',
            '  "parameters": ["D", "..."],',
            '  "parameter_conditions": ["..."],',
            '  "subsumed_signatures": ["..."],',
            '  "evidence_facets": [',
            "    {",
            '      "instance": "...",',
            '      "facet": "..."',
            "    }",
            "  ],",
            '  "expected_derivation_route": [',
            '    "residual",',
            '    "support relaxation",',
            '    "mixed MIR or MIR-over-MIR"',
            "  ],",
            '  "validation_plan": [',
            '    "instantiate on tested instances",',
            '    "exact normalized matching",',
            '    "finite validity check",',
            '    "derivation certificate check"',
            "  ],",
            '  "known_risks": ["..."],',
            '  "notes": "..."',
            "}",
            "```",
            "",
            "# Rules",
            "",
            "1. Prefer one general parameterized family over many local families.",
            "2. Do not hard-code one tested instance as a family.",
            "3. Do not claim validity merely from computational evidence.",
            "4. Do not add the family to derived families.",
            "5. Do not modify source code unless necessary.",
            "6. If the current clusters are too heterogeneous, propose several candidate families, but keep the number small.",
            "7. If no useful generalization is found, write a guess JSON with status `no_good_guess` and explain why.",
            "8. After a guess is later verified, derived (certificate produced), and backfilled, record the facets it covers in `memory/facets/"
            + problem_id
            + "/coverage.json` per the coverage protocol.",
            "",
            "# Expected final response",
            "",
            "Report:",
            "",
            "1. which guess file you wrote;",
            "2. which signatures or facets it tries to subsume;",
            "3. why the proposed family is more general than the local candidates;",
            "4. what the Verifier should check next.",
            "",
        ]
    )

    return _NL.join(lines)


def _build_verifier_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    problem_id = state.problem_id
    task = decision.selected_task or {}

    guess_file = str(task.get("guess_file", ""))
    verification_file = str(
        task.get(
            "verification_file",
            f"memory/family/{problem_id}/verifications/verification.json",
        )
    )

    lines: list[str] = []
    lines.extend(_goal_block(problem_id))
    lines.extend(_context_files(problem_id))
    lines.extend(_decision_block(decision))
    lines.extend(_selected_task_block(task))
    lines.extend(_coverage_protocol_block(problem_id))

    lines.extend(
        [
            "# Your role: Verifier",
            "",
            "You are not the family proposer.",
            "You are not trying to make the guess look good.",
            "Your job is to check whether the guessed symbolic family is well-formed enough to enter implementation, derivation, or rejection.",
            "",
            "# Files to inspect",
            "",
            f"- family guess: `{guess_file}`",
            f"- state file: `reports/{problem_id}_state.json`",
            f"- facet memory: `memory/facets/{problem_id}/facet_signatures.json`",
            f"- family memory: `memory/family/{problem_id}/family_memory.json`",
            "",
            "# Verification checklist",
            "",
            "Check the following:",
            "",
            "1. The symbolic statement is written in original problem notation, not only in one concrete instance.",
            "2. Parameters and parameter conditions are explicit.",
            "3. The family is not merely a renamed concrete facet.",
            "4. The claimed evidence facets actually match the proposed template informally.",
            "5. Exact instantiation matching appears implementable.",
            "6. Finite validity checking appears implementable.",
            "7. A plausible derivation route is specified.",
            "8. The derivation route does not obviously use invalid addition, overcounting, or unsupported MIR steps.",
            "9. The family should remain `candidate` unless a derivation certificate exists.",
            "",
            "# Output requirement",
            "",
            "Create or overwrite this JSON file:",
            "",
            f"`{verification_file}`",
            "",
            "Use this schema:",
            "",
            "```json",
            "{",
            '  "problem_id": "...",',
            '  "agent": "Verifier",',
            '  "guess_file": "...",',
            '  "verdict": "accept_for_implementation | needs_revision | invalid | insufficient",',
            '  "summary": "...",',
            '  "checks": {',
            '    "well_formed_symbolic_statement": true,',
            '    "explicit_parameters": true,',
            '    "not_over_specialized": true,',
            '    "evidence_matches_template": true,',
            '    "exact_matching_implementable": true,',
            '    "finite_validity_implementable": true,',
            '    "derivation_route_specified": true,',
            '    "obvious_invalid_step_found": false',
            "  },",
            '  "problems_found": ["..."],',
            '  "recommended_next_task": {',
            '    "type": "implement_family | revise_guess | derive_family | reject_family",',
            '    "target_files": ["..."],',
            '    "instructions": "..."',
            "  }",
            "}",
            "```",
            "",
            "# Required task-pool update",
            "",
            "If the verdict is `accept_for_implementation`, add a concrete open task to `tasks/TASK_POOL.json` with type `implement_family` or `derive_family`.",
            "",
            "If the verdict is `needs_revision`, add or update a task for FamilyGuesser explaining what must be revised.",
            "",
            "If the verdict is `invalid`, do not delete the guess. Keep the verification report as memory so the same bad family is not proposed again.",
            "",
            "If the verdict is `insufficient`, add concrete information request or refinement task.",
            "",
            "# Important: verdict semantics",
            "",
            "`accept_for_implementation` means the family is well-formed enough to enter",
            "implementation as a CANDIDATE. It does NOT mean the family is derived or",
            "proved. A family accepted with this verdict but without a derivation",
            "certificate file in `memory/family/"
            + problem_id
            + "/derivations/` will be",
            "dispatched to the DerivationProver next, NOT to coverage backfill.",
            "Coverage backfill only happens after a certificate file exists.",
            "",
            "# Expected final response",
            "",
            "Report:",
            "",
            "1. verdict;",
            "2. verification file written;",
            "3. main problems found;",
            "4. recommended next task;",
            "5. whether TASK_POOL.json was updated.",
            "",
        ]
    )

    return _NL.join(lines)


def _build_derivation_prover_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    problem_id = state.problem_id
    task = decision.selected_task or {}

    lines: list[str] = []
    lines.extend(_goal_block(problem_id))
    lines.extend(_context_files(problem_id))
    lines.extend(_decision_block(decision))
    lines.extend(_selected_task_block(task))
    lines.extend(_coverage_protocol_block(problem_id))

    lines.extend(
        [
            "# Your role: DerivationProver",
            "",
            "The Verifier has accepted symbolic families as candidates, but they",
            "still lack derivation certificates. Without a certificate, coverage",
            "cannot be recorded and the loop cannot converge. Your job is to",
            "produce a derivation certificate for each pending family, or a",
            "documented failure report if derivation is genuinely blocked.",
            "",
            "# What to do for each pending family",
            "",
            "1. Read the family guess file. It contains `expected_derivation_route`",
            "   and `validation_plan` describing the intended proof strategy.",
            "2. Follow that route using the documented derivation patterns:",
            "   residualization, coefficient tightening, aggregation, c-MIR,",
            "   mixed MIR, and MIR-over-MIR / derived-row reuse.",
            "3. Start from the source constraints named in the guess (e.g. the",
            "   two MALP activation rows `x(J1) >= b1 y1` and `x(J2) >= b2 y2`)",
            "   and the variable bounds.",
            "4. Reconstruct the target family inequality symbolically, naming",
            "   every intermediate derived row, the subsets/parameters chosen,",
            "   the rounding/mixing step, and the final coefficient tightening.",
            "5. On SUCCESS, write a certificate JSON file to:",
            "",
            f"   `memory/family/{problem_id}/derivations/<family_id>_certificate.json`",
            "",
            "   with this schema:",
            "",
            "```json",
            "{",
            '  "problem_id": "...",',
            '  "agent": "DerivationProver",',
            '  "family_id": "...",',
            '  "family_name": "...",',
            '  "status": "certified",',
            '  "guess_file": "...",',
            '  "verification_file": "...",',
            '  "source_constraints": ["activation_j1", "activation_j2", ...],',
            '  "steps": [',
            "    {",
            '      "method": "residualization | coefficient_tightening | aggregation | c_mir | mixed_mir | mir_over_mir",',
            '      "description": "...",',
            '      "expression": "...",',
            '      "intermediate_row": "..."',
            "    }",
            "  ],",
            '  "reconstructed_inequality": "symbolic form of the target",',
            '  "parameter_conditions": ["..."],',
            '  "limitations": ["..."]',
            "}",
            "```",
            "",
            "6. On FAILURE, write a failure JSON file to:",
            "",
            f"   `memory/family/{problem_id}/derivations/<family_id>_failure.json`",
            "",
            "   with this schema:",
            "",
            "```json",
            "{",
            '  "problem_id": "...",',
            '  "agent": "DerivationProver",',
            '  "family_id": "...",',
            '  "status": "failed",',
            '  "blocker_reason": "...",',
            '  "attempted_methods": ["..."],',
            '  "recommended_next_action": "revise_guess | new_family | deeper_mir | ..."',
            "}",
            "```",
            "",
            "# Critical constraints",
            "",
            "- The certificate file is the ONLY artifact the regulator reads to decide",
            "  whether the family is derived. Do NOT edit the study adapter or the",
            "  state JSON to mark the family as derived.",
            "- A failure report prevents the regulator from re-dispatching derivation",
            "  for this family indefinitely. Use it honestly when you are genuinely",
            "  blocked, but do not use it to avoid work.",
            "- Do not record coverage here. Coverage backfill happens automatically",
            "  in the next round once a certificate exists.",
            "- Keep problem-specific mathematics in the adapter/examples area. The",
            "  certificate file itself is generic and problem-agnostic in schema.",
            "",
            "# Expected final response",
            "",
            "Report:",
            "",
            "1. which families received a certificate (family_id list);",
            "2. which families received a failure report and the blocker reason;",
            "3. certificate/failure file paths written;",
            "4. the core derivation method used for each successful family;",
            "5. any assumptions or limitations noted in the certificate.",
            "",
        ]
    )

    return _NL.join(lines)


def _build_backfill_coverage_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    problem_id = state.problem_id
    task = decision.selected_task or {}

    lines: list[str] = []
    lines.extend(_goal_block(problem_id))
    lines.extend(_context_files(problem_id))
    lines.extend(_decision_block(decision))
    lines.extend(_selected_task_block(task))
    lines.extend(_coverage_protocol_block(problem_id))

    lines.extend(
        [
            "# Your role: CoverageBackfiller",
            "",
            "Certified symbolic families exist, but their covered computed facets",
            "are still NOT recorded in the coverage manifest. The study adapter's",
            "fixed classifier keeps recreating these facets as `candidate` every",
            "round, so the regulator's stop counters never decrease. Your job is",
            "to translate each CERTIFIED family into concrete coverage records.",
            "",
            "This is the pivotal step that makes the research loop converge.",
            "",
            "# What to do for each pending family",
            "",
            "Each pending family already has a derivation certificate file (shown",
            "in the task). You do NOT need to re-derive or re-verify the family.",
            "",
            "1. Read the family guess to understand its symbolic form and parameters.",
            "2. For every tested instance listed in `reports/"
            + problem_id
            + "_state.json`:",
            "   a. instantiate the symbolic family with valid parameter assignments;",
            "   b. normalize the instantiated inequality using the same normalization",
            "      the study adapter uses (GCD reduction, sense flipped to <=);",
            "   c. compare the normalized instantiation against EVERY computed facet",
            "      of that instance by exact coefficient/rhs/sense equality;",
            "   d. for each exact match, append ONE entry to the manifest `covered`",
            "      list with the normalized `inequality`, `family` set to the family_id,",
            "      and `source` set to the certificate file path.",
            "3. After processing a family, append its family_id to the manifest's",
            "   `backfilled_families` list so the regulator does not re-request it.",
            "",
            "# Critical constraints",
            "",
            "- Coverage is by EXACT normalized equality, never by visual similarity",
            "  or partial overlap. Reuse `psa.family.match_instantiation_to_facets`",
            "  semantics: instantiate -> normalize -> compare equality.",
            "- The families listed here are CERTIFIED. Do not re-check the certificate.",
            "- Do NOT delete existing entries; merge or append only.",
            "- If the manifest does not exist yet, create it with the shape shown in",
            "  the coverage protocol above, including `backfilled_families`.",
            "- Keep the problem-specific instantiation logic in the adapter/examples.",
            "  You may call into `examples/"
            + problem_id
            + "/families.py` or write small",
            "  problem-specific instantiation helpers; do not put problem-specific",
            "  mathematics into `src/psa/`.",
            "",
            "# If a family cannot be matched",
            "",
            "If instantiation or exact matching fails for a certified family,",
            "do not silently skip it. Write a short note under",
            "`memory/family/"
            + problem_id
            + "/backfill_notes/<family_id>.json` describing:",
            "- which family;",
            "- which instances failed;",
            "- whether the family statement needs parameter correction;",
            "- recommended next action (revise_guess or re-derive).",
            "",
            "# Expected final response",
            "",
            "Report:",
            "",
            "1. coverage manifest file written or updated;",
            "2. which families were backfilled (family_id list);",
            "3. how many covered facet entries were added in total;",
            "4. whether `backfilled_families` was appended correctly;",
            "5. whether any families had matching failures and where the notes were written.",
            "",
        ]
    )

    return _NL.join(lines)


def _build_final_report_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    problem_id = state.problem_id
    task = decision.selected_task or {}

    lines: list[str] = []
    lines.extend(_goal_block(problem_id))
    lines.extend(_context_files(problem_id))
    lines.extend(_decision_block(decision))
    lines.extend(_selected_task_block(task))

    lines.extend(
        [
            "# Your role: FinalReporter",
            "",
            "The research loop has converged: all computed nontrivial facets in the",
            "current tested scope are covered by derived symbolic families. Your job",
            "is to synthesize ALL artifacts produced during the loop into a single,",
            "complete, family-first research report for a human researcher to review.",
            "",
            "# Inputs to read",
            "",
            f"- Final state (post-overlay): `reports/{problem_id}_state.json`",
            f"- Coverage manifest: `memory/facets/{problem_id}/coverage.json`",
            f"- Derivation certificates: `memory/family/{problem_id}/derivations/`",
            f"- Family guesses: `memory/family/{problem_id}/guesses/`",
            f"- Verifications: `memory/family/{problem_id}/verifications/`",
            f"- Study adapter report (intermediate): `reports/{problem_id}_report.md`",
            f"- Facet signatures: `memory/facets/{problem_id}/facet_signatures.json`",
            f"- Problem description: `examples/{problem_id}/README.md`",
            "",
            "# What the report must contain",
            "",
            "Write a family-first markdown report following this structure:",
            "",
            "1. **Title and problem description**",
            "   - State the integer set being studied in original problem notation.",
            "   - List the tested scope (parameter ranges, tested sizes, backend).",
            "",
            "2. **Summary of results**",
            "   - Total instances tested, total computed facets.",
            "   - How many facets are covered by built-in families vs discovered families.",
            "   - Stop status and what it means (computational coverage, not a full theorem).",
            "",
            "3. **Derived or proved symbolic inequality families**",
            "   For EACH family (both built-in families from the study adapter and",
            "   discovered/certified families from the loop):",
            "   - family name and identifier",
            "   - symbolic statement in original problem notation (LaTeX or inline)",
            "   - parameter conditions",
            "   - validity status (how validity was checked: built-in, finite-validity, proved)",
            "   - derivation certificate (if any): summitmarize source constraints, key steps,",
            "     and the method used (residualization, aggregation, c-MIR, mixed MIR, etc.)",
            "   - coverage: how many computed facets this family covers, with a few examples",
            "   - facetness status and completeness status",
            "   - limitations and boundary cases",
            "",
            "4. **Derivation certificates**",
            "   For each certified family, include a compact summary of the certificate:",
            "   - source constraints",
            "   - key derivation steps with intermediate rows",
            "   - the reconstructed target inequality",
            "   - any limitations",
            "",
            "5. **Coverage summary**",
            "   - A table: family -> number of covered facets -> evidence source.",
            "   - Note that coverage is by exact normalized matching, not visual similarity.",
            "",
            "6. **Remaining proof obligations**",
            "   - What a full convex-hull theorem still requires:",
            "     a. validity proof for all admissible parameters (not just tested ones)",
            "     b. reverse-inclusion proof (the proposed relaxation is contained in conv(X))",
            "     c. parameter ranges where each family is facet-defining",
            "   - Any families that failed derivation and their blocker reasons.",
            "",
            "7. **Computational evidence appendix**",
            "   - Instance count, facet count per relation type (disjoint/overlap/nested/identical).",
            "   - A sample of covered facets with their instance labels.",
            "   - Any backfill notes or matching failures recorded.",
            "",
            "# Writing rules",
            "",
            "- Use the original problem notation from `examples/" + problem_id + "/README.md`.",
            "- Do NOT present raw cddlib facets as the final result.",
            "- Do NOT claim a complete convex hull description without a reverse-inclusion proof.",
            "- Distinguish built-in/standard families (variable bounds, activation rows,",
            "  residuals) from newly discovered/certified families.",
            "- If a family was discovered by the agent loop, cite the guess file,",
            "  verification file, and certificate file paths.",
            "- The report is for a human researcher. Be precise but readable.",
            "",
            "# Output requirement",
            "",
            f"Write the report to: `{task.get('output_path', f'reports/{problem_id}_final_report.md')}`",
            "",
            "# Expected final response",
            "",
            "Report:",
            "",
            "1. the output path of the final report;",
            "2. which families were included;",
            "3. the total facet coverage count;",
            "4. any sections where information was incomplete.",
            "",
        ]
    )

    return _NL.join(lines)


def _build_generic_executor_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    problem_id = state.problem_id
    task = decision.selected_task

    lines: list[str] = []
    lines.extend(_goal_block(problem_id))
    lines.extend(_context_files(problem_id))
    lines.extend(_decision_block(decision))
    lines.extend(_selected_task_block(task))
    lines.extend(_coverage_protocol_block(problem_id))

    lines.extend(
        [
            "# Work instructions",
            "",
            "Please make the smallest useful repository changes needed for the selected task.",
            "",
            "Rules:",
            "",
            "1. Do not move problem-specific logic into `src/psa/` unless it is genuinely reusable.",
            "2. Do not mark a candidate family as derived without a derivation certificate.",
            "3. Do not count visual similarity as coverage. Use exact normalized matching.",
            "4. Do not rely only on tiny instances if a family appears over-specialized.",
            "5. If many local candidate families have similar form, perform a family-compression pass.",
            "6. For interaction facets, try derived-row reuse / MIR-over-MIR before declaring unresolved.",
            "7. After modifying code, rerun the relevant study command and tests.",
            "8. When a family is certified and backfilled, record the facets it covers in",
            f"   `memory/facets/{problem_id}/coverage.json` so the loop can converge.",
            "",
            "# Expected final response",
            "",
            "At the end of this task, report:",
            "",
            "1. files changed;",
            "2. tests or study commands run;",
            "3. whether candidate/unresolved counts decreased (and coverage.json updated);",
            "4. which task id was completed or remains open;",
            "5. next blocker if any.",
            "",
        ]
    )

    return _NL.join(lines)


def write_next_prompt(
    *,
    project_root: Path,
    problem_id: str,
    prompt: str,
) -> Path:
    path = project_root / "reports" / f"next_{problem_id}_claude_task.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(prompt, encoding="utf-8")

    latest = project_root / "reports" / "next_claude_task.md"
    latest.write_text(prompt, encoding="utf-8")

    return path

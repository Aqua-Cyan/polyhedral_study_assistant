from __future__ import annotations

from pathlib import Path
from typing import Any

from psa.agent.regulator import RegulatorDecision
from psa.agent.state import ResearchState


def build_next_claude_prompt(
    *,
    project_root: Path,
    state: ResearchState,
    decision: RegulatorDecision,
) -> str:
    next_agent = decision.next_agent or "ClaudeCode"

    if next_agent == "FamilyGuesser":
        return _build_family_guesser_prompt(
            project_root=project_root,
            state=state,
            decision=decision,
        )

    if next_agent == "Verifier":
        return _build_verifier_prompt(
            project_root=project_root,
            state=state,
            decision=decision,
        )

    return _build_generic_executor_prompt(
        project_root=project_root,
        state=state,
        decision=decision,
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
        "- `docs/facet-analysis.md` if present",
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
        lines.extend(
            [
                "## Guess file",
                "",
                f"- `{task['guess_file']}`",
                "",
            ]
        )

    if "verification_file" in task:
        lines.extend(
            [
                "## Verification file to write",
                "",
                f"- `{task['verification_file']}`",
                "",
            ]
        )

    if "signature" in task:
        lines.extend(
            [
                "## Facet signature",
                "",
                f"`{task['signature']}`",
                "",
            ]
        )

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
            "- residual expressions such as `b - |J \\ D|`; ",
            "- MIR-over-MIR or derived-row reuse routes.",
            "",
            "# Output requirement",
            "",
            f"Create or overwrite this JSON file:",
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
            '      "facet": "...",',
            '      "parameter_values": {"D": "..."}',
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

    return "\n".join(lines)


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
            f"Create or overwrite this JSON file:",
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
            "# Optional task-pool update",
            "",
            "If the verdict is `accept_for_implementation`, add a concrete open task to `tasks/TASK_POOL.json` with type `implement_family` or `derive_family`.",
            "",
            "If the verdict is `needs_revision`, add or update a task for FamilyGuesser explaining what must be revised.",
            "",
            "If the verdict is `invalid`, do not delete the guess. Keep the verification report as memory so the same bad family is not proposed again.",
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

    return "\n".join(lines)


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
            "",
            "# Expected final response",
            "",
            "At the end of this task, report:",
            "",
            "1. files changed;",
            "2. tests or study commands run;",
            "3. whether candidate/unresolved counts decreased;",
            "4. which task id was completed or remains open;",
            "5. next blocker if any.",
            "",
        ]
    )

    return "\n".join(lines)


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

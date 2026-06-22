from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from psa.agent.state import ResearchState


@dataclass(frozen=True)
class RegulatorDecision:
    decision: str
    reason: str
    selected_task: dict[str, Any] | None
    next_agent: str | None
    success_criterion: str
    stop: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "reason": self.reason,
            "selected_task": self.selected_task,
            "next_agent": self.next_agent,
            "success_criterion": self.success_criterion,
            "stop": self.stop,
        }


class SingleRegulator:
    """A deterministic research-loop regulator.

    The regulator does not prove inequalities and does not guess families.
    It only decides what role should act next.

    Stage 3 roles:

    - FamilyGuesser:
        groups many candidate facets and proposes a more general symbolic family.
        It writes guess JSON files to memory/family/<problem_id>/guesses/.

    - Verifier:
        checks an unverified guess and writes a verification report to
        memory/family/<problem_id>/verifications/.

    - DerivationProver:
        tries to derive a concrete facet/family using residual, tightening,
        mixed MIR, or MIR-over-MIR.

    The regulator itself should not be scheduled as a normal Claude Code task.
    """

    def decide(self, state: ResearchState) -> RegulatorDecision:
        if not state.raw_state:
            return RegulatorDecision(
                decision="RUN_STUDY_FIRST",
                reason=(
                    "No research state was found. Run the problem adapter first "
                    "to generate reports/<problem>_state.json."
                ),
                selected_task=None,
                next_agent="StudyAdapter",
                success_criterion="Generate state, report, task pool, and memory files.",
                stop=False,
            )

        unverified_guess_task = self._build_unverified_guess_task(state)
        if unverified_guess_task is not None:
            return RegulatorDecision(
                decision="VERIFY_FAMILY_GUESS",
                reason=(
                    "A family guess exists without a corresponding verifier report. "
                    "Before asking for more guesses or derivations, verify the current guess."
                ),
                selected_task=unverified_guess_task,
                next_agent="Verifier",
                success_criterion=unverified_guess_task["success_criterion"],
                stop=False,
            )

        if self._is_done(state):
            return RegulatorDecision(
                decision="DONE",
                reason=(
                    "The current tested scope has no candidate or unresolved facet records, "
                    "and there are no unverified family guesses. The computational loop is "
                    "complete for the current tested scope. A full convex-hull theorem still "
                    "requires a mathematical completeness proof."
                ),
                selected_task=None,
                next_agent=None,
                success_criterion="No further loop task required for the current tested scope.",
                stop=True,
            )

        open_tasks = self._concrete_open_tasks(state.open_tasks)

        if not open_tasks:
            return RegulatorDecision(
                decision="BLOCKED_NO_CONCRETE_TASKS",
                reason=(
                    "The state indicates continuation is needed, but no concrete open task "
                    "exists for this problem in TASK_POOL.json. Regulator/meta tasks are ignored."
                ),
                selected_task=None,
                next_agent="Regulator",
                success_criterion=(
                    "Regenerate TASK_POOL.json from the study adapter, or add concrete tasks "
                    "such as family_compression, derive_interaction_family, or "
                    "analyze_unresolved_signature."
                ),
                stop=False,
            )

        selected = self._select_task(state, open_tasks)
        task_type = str(selected.get("type", ""))
        assigned_agent = str(selected.get("assigned_agent", "ClaudeCode"))

        if task_type == "family_compression":
            decision = "RUN_FAMILY_GUESSER"
            next_agent = "FamilyGuesser"
        elif task_type == "derive_interaction_family":
            decision = "DERIVE_INTERACTION"
            next_agent = assigned_agent if assigned_agent != "Regulator" else "DerivationProver"
        elif task_type == "analyze_unresolved_signature":
            decision = "ANALYZE_UNRESOLVED"
            next_agent = assigned_agent if assigned_agent != "Regulator" else "DerivationProver"
        elif task_type == "verify_family_guess":
            decision = "VERIFY_FAMILY_GUESS"
            next_agent = "Verifier"
        else:
            decision = "CONTINUE_SELECTED_TASK"
            next_agent = assigned_agent

        return RegulatorDecision(
            decision=decision,
            reason=self._build_reason(state, selected),
            selected_task=selected,
            next_agent=next_agent,
            success_criterion=str(
                selected.get(
                    "success_criterion",
                    "Make measurable progress on the selected research task.",
                )
            ),
            stop=False,
        )

    def _is_done(self, state: ResearchState) -> bool:
        if state.stop_status == "done":
            return True

        return state.candidate_count == 0 and state.unresolved_count == 0

    def _build_unverified_guess_task(self, state: ResearchState) -> dict[str, Any] | None:
        unverified = state.unverified_guess_files()
        if not unverified:
            return None

        guess_file = unverified[0]
        relative_guess_file = self._relative_path(guess_file, state.project_root)

        return {
            "id": f"{state.problem_id}-verify-{guess_file.stem}",
            "problem_id": state.problem_id,
            "type": "verify_family_guess",
            "status": "open",
            "priority": 0,
            "assigned_agent": "Verifier",
            "guess_file": relative_guess_file,
            "verification_file": (
                f"memory/family/{state.problem_id}/verifications/"
                f"{guess_file.stem}_verification.json"
            ),
            "required_actions": [
                "read the family guess JSON",
                "check whether the symbolic statement is well-formed",
                "check whether parameters and conditions are explicit",
                "check whether the guess subsumes the claimed facet signatures",
                "check whether exact instantiation matching is implementable",
                "check whether finite validity testing is implementable",
                "check whether a derivation route is specified",
                "write a verifier report JSON",
                "recommend accept_for_implementation, needs_revision, invalid, or insufficient",
            ],
            "success_criterion": (
                "Produce a verifier report JSON with a clear verdict and concrete next action."
            ),
        }

    def _concrete_open_tasks(self, tasks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            task
            for task in tasks
            if task.get("type") != "regulator_decision"
        ]

    def _select_task(self, state: ResearchState, tasks: list[dict[str, Any]]) -> dict[str, Any]:
        """Select the next concrete research task.

        Policy:

        1. If many candidate facets remain, prefer family_compression.
        2. Otherwise derive interaction families.
        3. Then analyze unresolved signatures.
        4. Fall back to priority order.
        """
        family_compression = [
            task for task in tasks
            if task.get("type") == "family_compression"
        ]

        if state.candidate_count >= 20 and family_compression:
            return sorted(
                family_compression,
                key=lambda task: (
                    int(task.get("priority", 999)),
                    str(task.get("id", "")),
                ),
            )[0]

        derive_interaction = [
            task for task in tasks
            if task.get("type") == "derive_interaction_family"
        ]

        if derive_interaction:
            return sorted(
                derive_interaction,
                key=self._task_rank_key,
            )[0]

        analyze_unresolved = [
            task for task in tasks
            if task.get("type") == "analyze_unresolved_signature"
        ]

        if analyze_unresolved:
            return sorted(
                analyze_unresolved,
                key=self._task_rank_key,
            )[0]

        if family_compression:
            return sorted(
                family_compression,
                key=self._task_rank_key,
            )[0]

        return sorted(tasks, key=self._task_rank_key)[0]

    def _task_rank_key(self, task: dict[str, Any]) -> tuple[int, int, str]:
        priority = int(task.get("priority", 999))
        facet_count = -int(task.get("facet_count", 0))
        task_id = str(task.get("id", ""))
        return (priority, facet_count, task_id)

    def _build_reason(self, state: ResearchState, task: dict[str, Any]) -> str:
        return (
            f"Research is not complete: candidate_records={state.candidate_count}, "
            f"unresolved_records={state.unresolved_count}, "
            f"signature_count={state.signature_count}. "
            f"Selected concrete task `{task.get('id')}` "
            f"of type `{task.get('type')}`."
        )

    def _relative_path(self, path: Path, root: Path) -> str:
        try:
            return str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")
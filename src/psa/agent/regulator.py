# src/psa/agent/regulator.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from psa.agent.state import ResearchState
from psa.coverage import load_backfilled_families


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
    """Deterministic research-loop regulator.

    Priority chain
    --------------
    1. No state                       -> RUN_STUDY_FIRST
    2. Unverified family guesses      -> VERIFY_FAMILY_GUESS
    3. Accepted but no certificate    -> NEEDS_DERIVATION
    4. Certified, not yet backfilled   -> BACKFILL_COVERAGE
    5. All facets covered, no report  -> WRITE_FINAL_REPORT   (new)
    6. All facets covered, report done-> DONE
    7. No concrete open tasks         -> BLOCKED_NO_CONCRETE_TASKS
    8. Select highest-priority task from pool
    """

    def decide(self, state: ResearchState) -> RegulatorDecision:
        if not state.raw_state:
            return RegulatorDecision(
                decision="RUN_STUDY_FIRST",
                reason=(
                    "No research state was found. Run the problem adapter first "
                    "to generate reports/_state.json."
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

        derivation_task = self._build_needs_derivation_task(state)
        if derivation_task is not None:
            return RegulatorDecision(
                decision="NEEDS_DERIVATION",
                reason=(
                    "There are verifier-accepted families that still lack a derivation "
                    "certificate, and there are still candidate or unresolved facets to "
                    "prune. Produce derivation certificates first; only then can coverage "
                    "be backfilled and the stop counters reduced."
                ),
                selected_task=derivation_task,
                next_agent="DerivationProver",
                success_criterion=derivation_task["success_criterion"],
                stop=False,
            )

        backfill_task = self._build_backfill_coverage_task(state)
        if backfill_task is not None:
            return RegulatorDecision(
                decision="BACKFILL_COVERAGE",
                reason=(
                    "There are certified symbolic families whose covered computed "
                    "facets are not yet recorded in the coverage manifest, but there "
                    "are still candidate or unresolved facets to prune. Backfill the "
                    "coverage manifest so the overlay can reduce the stop counters."
                ),
                selected_task=backfill_task,
                next_agent="CoverageBackfiller",
                success_criterion=backfill_task["success_criterion"],
                stop=False,
            )

        if self._is_done(state):
            return self._handle_done(state)

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
        elif task_type == "verify_family_guess":
            decision = "VERIFY_FAMILY_GUESS"
            next_agent = "Verifier"
        elif task_type in {"derive_family", "derive_interaction_family"}:
            decision = "DERIVE_FAMILY"
            next_agent = assigned_agent if assigned_agent != "Regulator" else "DerivationProver"
        elif task_type == "implement_family":
            decision = "IMPLEMENT_FAMILY"
            next_agent = assigned_agent if assigned_agent != "Regulator" else "DerivationProver"
        elif task_type == "revise_guess":
            decision = "REVISE_FAMILY_GUESS"
            next_agent = "FamilyGuesser"
        elif task_type == "analyze_unresolved_signature":
            decision = "ANALYZE_UNRESOLVED"
            next_agent = assigned_agent if assigned_agent != "Regulator" else "DerivationProver"
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

    def _handle_done(self, state: ResearchState) -> RegulatorDecision:
        """After all facets are covered, ensure a final report is produced.

        If no final report exists yet, dispatch a report-writing task instead
        of stopping. On the next round, when the report file is found, the
        loop stops cleanly and prints the report path.
        """
        report_path = state.final_report_path
        if not report_path.exists():
            task = self._build_final_report_task(state)
            return RegulatorDecision(
                decision="WRITE_FINAL_REPORT",
                reason=(
                    "All computed nontrivial facets in the current tested scope are "
                    "covered by derived symbolic families, but no final research report "
                    "has been produced yet. Write the family-first final report before "
                    "stopping."
                ),
                selected_task=task,
                next_agent="FinalReporter",
                success_criterion=task["success_criterion"],
                stop=False,
            )

        return RegulatorDecision(
            decision="DONE",
            reason=(
                "The current tested scope has no candidate or unresolved facet "
                "records, all families are backfilled, and the final report is at "
                f"{report_path.relative_to(state.project_root)}. "
                "The computational loop is complete for the current tested scope. "
                "A full convex-hull theorem still requires a mathematical "
                "completeness proof."
            ),
            selected_task=None,
            next_agent=None,
            success_criterion=(
                "No further loop task required for the current tested scope."
            ),
            stop=True,
        )

    def _build_final_report_task(self, state: ResearchState) -> dict[str, Any]:
        return {
            "id": f"{state.problem_id}-final-report",
            "problem_id": state.problem_id,
            "type": "write_final_report",
            "status": "open",
            "priority": 0,
            "assigned_agent": "FinalReporter",
            "state_file": str(
                state.state_path.relative_to(state.project_root).as_posix()
            ),
            "coverage_manifest": str(
                state.coverage_manifest_path.relative_to(state.project_root).as_posix()
            ),
            "derivations_dir": str(
                state.derivations_dir.relative_to(state.project_root).as_posix()
            )
            if state.derivations_dir.is_relative_to(state.project_root)
            else str(state.derivations_dir),
            "guesses_dir": str(
                state.guess_dir.relative_to(state.project_root).as_posix()
            )
            if state.guess_dir.is_relative_to(state.project_root)
            else str(state.guess_dir),
            "verifications_dir": str(
                state.verification_dir.relative_to(state.project_root).as_posix()
            )
            if state.verification_dir.is_relative_to(state.project_root)
            else str(state.verification_dir),
            "output_path": str(
                state.final_report_path.relative_to(state.project_root).as_posix()
            )
            if state.final_report_path.is_relative_to(state.project_root)
            else str(state.final_report_path),
            "certified_families": [
                {
                    "family_id": r["family_id"],
                    "family_name": r["family_name"],
                    "certificate_file": r["certificate_file"],
                }
                for r in state.accepted_family_records()
            ],
            "required_actions": [
                "read the overlay-applied state JSON for final summary and covered facets",
                "read the coverage manifest for per-facet coverage records",
                "read each derivation certificate for source constraints and proof steps",
                "read each family guess for the symbolic statement and parameter conditions",
                "read each verification file for the verifier's checks and notes",
                "synthesize all findings into a family-first markdown report",
                "include symbolic statements, parameter conditions, derivation certificates, coverage counts, test scope, remaining proof obligations",
                "write the report to the output path",
            ],
            "success_criterion": (
                "Produce a complete, human-readable family-first research report "
                "at the output path, suitable for a researcher to review."
            ),
        }

    def _build_needs_derivation_task(self, state: ResearchState) -> dict[str, Any] | None:
        if state.candidate_count == 0 and state.unresolved_count == 0:
            return None
        pending = state.accepted_but_uncertified_records()
        if not pending:
            return None
        derivations_dir = state.derivations_dir
        rel_dir = self._relative_path(derivations_dir, state.project_root)

        return {
            "id": f"{state.problem_id}-needs-derivation",
            "problem_id": state.problem_id,
            "type": "derive_family",
            "status": "open",
            "priority": 0,
            "assigned_agent": "DerivationProver",
            "pending_families": [
                {
                    "family_id": r["family_id"],
                    "family_name": r["family_name"],
                    "verification_file": r["verification_file"],
                    "guess_file": r["guess_file"],
                }
                for r in pending
            ],
            "derivations_dir": rel_dir,
            "required_actions": [
                "for each pending accepted family, attempt a derivation certificate",
                "follow the expected_derivation_route recorded in the guess file",
                "use residualization, coefficient tightening, aggregation, c-MIR, mixed MIR, or MIR-over-MIR as appropriate",
                "on success: write a certificate JSON to the derivations directory with family_id, status 'certified', source rows, steps, and the reconstructed target inequality",
                "on failure: write a failure JSON to the derivations directory with family_id, status 'failed', and the blocker reason",
                "do not mark the family as derived in the study adapter; the certificate file is the only artifact the regulator reads",
            ],
            "success_criterion": (
                "Produce a derivation certificate file for every pending family, "
                "or a documented failure report. Once a certificate exists, the "
                "next round will dispatch BACKFILL_COVERAGE for that family."
            ),
        }

    def _build_backfill_coverage_task(self, state: ResearchState) -> dict[str, Any] | None:
        if state.candidate_count == 0 and state.unresolved_count == 0:
            return None
        accepted = state.accepted_family_records()
        if not accepted:
            return None
        backfilled = load_backfilled_families(state.project_root, state.problem_id)
        pending = [r for r in accepted if r["family_id"] not in backfilled]
        if not pending:
            return None

        return {
            "id": f"{state.problem_id}-backfill-coverage",
            "problem_id": state.problem_id,
            "type": "backfill_coverage",
            "status": "open",
            "priority": 0,
            "assigned_agent": "CoverageBackfiller",
            "pending_families": [
                {
                    "family_id": r["family_id"],
                    "family_name": r["family_name"],
                    "verification_file": r["verification_file"],
                    "guess_file": r["guess_file"],
                    "certificate_file": r["certificate_file"],
                }
                for r in pending
            ],
            "coverage_manifest": str(
                state.coverage_manifest_path.relative_to(state.project_root).as_posix()
            ),
            "state_file": str(
                state.state_path.relative_to(state.project_root).as_posix()
            ),
            "required_actions": [
                "for each pending certified family, instantiate it on every tested instance",
                "match instantiated inequalities against the computed facets by exact normalized equality",
                "append each matched computed facet to the coverage manifest `covered` list",
                "append the family_id to the manifest `backfilled_families` list",
                "the family has a certificate file; do NOT re-check the certificate here",
            ],
            "success_criterion": (
                "Record covered facets for every pending certified family, and mark "
                "those families backfilled, so the next overlay reduces "
                "candidate/unresolved counts."
            ),
        }

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
        return [task for task in tasks if task.get("type") != "regulator_decision"]

    def _select_task(self, state: ResearchState, tasks: list[dict[str, Any]]) -> dict[str, Any]:
        followup_tasks = [
            task
            for task in tasks
            if task.get("type") in {"derive_family", "implement_family", "revise_guess"}
        ]
        if followup_tasks:
            return sorted(followup_tasks, key=self._task_rank_key)[0]

        family_compression = [task for task in tasks if task.get("type") == "family_compression"]
        if state.candidate_count >= 20 and family_compression:
            return sorted(
                family_compression,
                key=lambda task: (int(task.get("priority", 999)), str(task.get("id", ""))),
            )[0]

        derive_interaction = [task for task in tasks if task.get("type") == "derive_interaction_family"]
        if derive_interaction:
            return sorted(derive_interaction, key=self._task_rank_key)[0]

        analyze_unresolved = [task for task in tasks if task.get("type") == "analyze_unresolved_signature"]
        if analyze_unresolved:
            return sorted(analyze_unresolved, key=self._task_rank_key)[0]

        if family_compression:
            return sorted(family_compression, key=self._task_rank_key)[0]

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
            f"covered_records={state.covered_count}, "
            f"signature_count={state.signature_count}. "
            f"Selected concrete task `{task.get('id')}` "
            f"of type `{task.get('type')}`."
        )

    def _relative_path(self, path: Path, root: Path) -> str:
        try:
            return str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            return str(path).replace("\\", "/")

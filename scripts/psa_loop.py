from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

for path in (PROJECT_ROOT, SRC_ROOT):
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)

from psa.agent.executors import ClaudeCodeExecutor
from psa.agent.prompt_builder import build_next_claude_prompt, write_next_prompt
from psa.agent.regulator import SingleRegulator
from psa.agent.state import load_research_state, write_json
from psa.coverage import apply_coverage_to_state_file


def run_study_adapter(problem_id: str, max_size: int) -> None:
    command = [
        sys.executable,
        str(PROJECT_ROOT / "scripts" / "study.py"),
        "--problem",
        problem_id,
        "--max-size",
        str(max_size),
    ]

    print("Running study adapter:")
    print(" ".join(command))

    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def apply_coverage_overlay(problem_id: str) -> None:
    """Overlay the persistent coverage manifest onto the freshly written state.

    The study adapter recomputes the state from a fixed classifier every round,
    so families the agent proved during earlier rounds are not reflected. This
    overlay prunes covered facets from candidate/unresolved so the regulator's
    stop counters can actually reach zero.
    """
    state_path = PROJECT_ROOT / "reports" / f"{problem_id}_state.json"
    if not state_path.exists():
        return
    apply_coverage_to_state_file(PROJECT_ROOT, problem_id, state_path)
    print(f"Applied coverage overlay to {state_path}")


def run_one_regulator_round(
    *,
    problem_id: str,
    max_size: int,
    skip_study: bool,
    execute: bool,
    executor_command: str | None,
    executor_timeout: int,
    round_index: int,
) -> bool:
    """Run one regulated research-loop round.

    Returns True if the outer loop should continue.
    Returns False if the loop should stop.
    """
    if not skip_study:
        run_study_adapter(problem_id=problem_id, max_size=max_size)

    # Close the coverage feedback loop before the regulator reads the state.
    apply_coverage_overlay(problem_id=problem_id)

    state = load_research_state(
        project_root=PROJECT_ROOT,
        problem_id=problem_id,
    )

    regulator = SingleRegulator()
    decision = regulator.decide(state)

    decision_path = PROJECT_ROOT / "reports" / "regulator_decision.json"
    write_json(decision_path, decision.to_dict())

    print("")
    print("Regulator decision:")
    print(json.dumps(decision.to_dict(), indent=2, ensure_ascii=False))

    if decision.stop:
        print("")
        print("Research loop status: DONE for current tested scope.")
        return False

    prompt = build_next_claude_prompt(
        project_root=PROJECT_ROOT,
        state=state,
        decision=decision,
    )

    prompt_path = write_next_prompt(
        project_root=PROJECT_ROOT,
        problem_id=problem_id,
        prompt=prompt,
    )

    print("")
    print("Research loop status: CONTINUE")
    print(f"Next Claude task written to: {prompt_path}")
    print(f"Stable prompt path: {PROJECT_ROOT / 'reports' / 'next_claude_task.md'}")

    if not execute:
        print("")
        print("Execution mode: disabled")
        print("Next step:")
        print("Paste reports/next_claude_task.md into Claude Code, or rerun with --execute.")
        return False

    print("")
    print("Execution mode: enabled")
    print("Sending prompt to Claude Code...")

    executor = ClaudeCodeExecutor(
        project_root=PROJECT_ROOT,
        command_template=executor_command,
        timeout_seconds=executor_timeout,
    )

    result = executor.run(
        prompt=prompt,
        prompt_path=prompt_path,
        problem_id=problem_id,
        decision=decision.decision,
        round_index=round_index,
    )

    result_path = PROJECT_ROOT / "reports" / "last_claude_execution.json"
    write_json(result_path, result.to_dict())

    print("")
    print("Claude Code execution result:")
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    if not result.succeeded:
        print("")
        print("Claude Code execution failed or timed out.")
        print("Check the stdout/stderr logs above before continuing.")
        return False

    print("")
    print("Claude Code execution succeeded.")
    print("The next loop round will rerun the study adapter and re-evaluate the state.")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a regulated PSA research-loop iteration.")

    parser.add_argument(
        "--problem",
        required=True,
        help="Problem id, e.g. malp.",
    )

    parser.add_argument(
        "--max-size",
        type=int,
        default=5,
        help="Size parameter passed to scripts/study.py.",
    )

    parser.add_argument(
        "--skip-study",
        action="store_true",
        help=(
            "Skip the study adapter only for the first round. "
            "If --execute and --rounds > 1 are used, later rounds rerun the study."
        ),
    )

    parser.add_argument(
        "--execute",
        action="store_true",
        help="Automatically send the generated prompt to the configured Claude Code command.",
    )

    parser.add_argument(
        "--executor-command",
        default=None,
        help=(
            "Command used to invoke Claude Code. "
            "Default comes from PSA_CLAUDE_COMMAND or 'claude --print'. "
            "The prompt is passed through stdin unless the command contains {prompt_file}."
        ),
    )

    parser.add_argument(
        "--executor-timeout",
        type=int,
        default=3600,
        help="Timeout in seconds for one Claude Code execution.",
    )

    parser.add_argument(
        "--rounds",
        type=int,
        default=1,
        help=(
            "Maximum number of regulated rounds to run. "
            "Use with --execute for automatic multi-round research."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.rounds < 1:
        raise ValueError("--rounds must be at least 1")

    for round_index in range(1, args.rounds + 1):
        print("")
        print("=" * 80)
        print(f"PSA regulated loop round {round_index}/{args.rounds}")
        print("=" * 80)

        skip_study_this_round = args.skip_study and round_index == 1

        should_continue = run_one_regulator_round(
            problem_id=args.problem,
            max_size=args.max_size,
            skip_study=skip_study_this_round,
            execute=args.execute,
            executor_command=args.executor_command,
            executor_timeout=args.executor_timeout,
            round_index=round_index,
        )

        if not should_continue:
            break

        if not args.execute:
            break

    print("")
    print("PSA loop finished.")


if __name__ == "__main__":
    main()

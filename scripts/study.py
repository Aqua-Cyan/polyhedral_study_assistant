from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

# Make repository root importable when running:
#   python scripts/study.py --problem malp
#
# Without this, Python sees scripts/ as the import root and cannot import
# examples.malp.study.
for path in (PROJECT_ROOT, SRC_ROOT):
    text = str(path)
    if text not in sys.path:
        sys.path.insert(0, text)

def problem_dir(problem_id: str) -> Path:
    return PROJECT_ROOT / "examples" / problem_id


def problem_readme(problem_id: str) -> Path:
    return problem_dir(problem_id) / "README.md"


def adapter_module_name(problem_id: str) -> str:
    return f"examples.{problem_id}.study"


def ensure_problem_exists(problem_id: str) -> None:
    directory = problem_dir(problem_id)
    readme = problem_readme(problem_id)

    if not directory.exists():
        raise FileNotFoundError(
            f"Problem directory does not exist: {directory}\n"
            f"Create examples/{problem_id}/README.md first."
        )

    if not readme.exists():
        raise FileNotFoundError(
            f"Problem README does not exist: {readme}\n"
            f"The user should define the set in examples/{problem_id}/README.md."
        )


def load_adapter(problem_id: str):
    module_name = adapter_module_name(problem_id)
    expected_file = problem_dir(problem_id) / "study.py"

    if not expected_file.exists():
        raise ModuleNotFoundError(
            f"No study adapter file found for problem `{problem_id}`.\n\n"
            f"Expected file: {expected_file}\n\n"
            "Next step: ask Claude Code to generate a thin problem-specific adapter "
            f"from examples/{problem_id}/README.md."
        )

    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            f"Could not import study adapter for problem `{problem_id}`.\n\n"
            f"Expected module: {module_name}\n"
            f"Expected file: examples/{problem_id}/study.py\n\n"
            f"Repository root on sys.path: {PROJECT_ROOT}\n\n"
            "If the file exists, check that examples/__init__.py and "
            f"examples/{problem_id}/__init__.py exist, and that the adapter imports are valid."
        ) from exc


def run_problem(problem_id: str, max_size: int) -> dict[str, Any]:
    ensure_problem_exists(problem_id)
    adapter = load_adapter(problem_id)

    if not hasattr(adapter, "run"):
        raise AttributeError(
            f"Adapter examples/{problem_id}/study.py must expose a function:\n\n"
            f"    run(max_union_size: int) -> dict\n\n"
            f"or a compatible run(...) function."
        )

    return adapter.run(max_union_size=max_size)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a problem-specific convex-hull study adapter.")
    parser.add_argument(
        "--problem",
        required=True,
        help="Problem id, e.g. malp. Expects examples/<problem>/README.md and examples/<problem>/study.py.",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=5,
        help="Size parameter passed to the problem adapter.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    state = run_problem(problem_id=args.problem, max_size=args.max_size)

    print("")
    print("Study adapter finished.")
    print(json.dumps(state.get("summary", state), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

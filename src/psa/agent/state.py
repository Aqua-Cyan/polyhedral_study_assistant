from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ResearchState:
    problem_id: str
    project_root: Path
    state_path: Path
    task_pool_path: Path
    raw_state: dict[str, Any]
    task_pool: list[dict[str, Any]]

    @property
    def summary(self) -> dict[str, Any]:
        return self.raw_state.get("summary", {})

    @property
    def stop_status(self) -> str:
        return str(self.summary.get("stop_status", "continue"))

    @property
    def candidate_count(self) -> int:
        return int(self.summary.get("candidate_records", 0))

    @property
    def unresolved_count(self) -> int:
        return int(self.summary.get("unresolved_records", 0))

    @property
    def derived_count(self) -> int:
        return int(self.summary.get("derived_records", 0))

    @property
    def signature_count(self) -> int:
        return int(self.summary.get("signature_count", 0))

    @property
    def family_memory_dir(self) -> Path:
        return self.project_root / "memory" / "family" / self.problem_id

    @property
    def guess_dir(self) -> Path:
        return self.family_memory_dir / "guesses"

    @property
    def verification_dir(self) -> Path:
        return self.family_memory_dir / "verifications"

    @property
    def open_tasks(self) -> list[dict[str, Any]]:
        return [
            task
            for task in self.task_pool
            if task.get("problem_id") == self.problem_id
            and task.get("status", "open") == "open"
        ]

    def unverified_guess_files(self) -> list[Path]:
        """Return family guesses that do not yet have a verifier report.

        FamilyGuesser is expected to write files under:

            memory/family/<problem_id>/guesses/*.json

        Verifier is expected to write corresponding files under:

            memory/family/<problem_id>/verifications/<guess_stem>_verification.json
        """
        if not self.guess_dir.exists():
            return []

        guess_files = sorted(self.guess_dir.glob("*.json"))
        unverified: list[Path] = []

        for guess_file in guess_files:
            verification_file = self.verification_dir / f"{guess_file.stem}_verification.json"
            if not verification_file.exists():
                unverified.append(guess_file)

        return unverified


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON file: {path}") from exc


def load_research_state(
    *,
    project_root: Path,
    problem_id: str,
) -> ResearchState:
    state_path = project_root / "reports" / f"{problem_id}_state.json"
    task_pool_path = project_root / "tasks" / "TASK_POOL.json"

    raw_state = load_json(state_path, default={})
    task_pool = load_json(task_pool_path, default=[])

    if not isinstance(raw_state, dict):
        raise ValueError(f"State file must contain a JSON object: {state_path}")

    if not isinstance(task_pool, list):
        raise ValueError(f"Task pool must contain a JSON list: {task_pool_path}")

    return ResearchState(
        problem_id=problem_id,
        project_root=project_root,
        state_path=state_path,
        task_pool_path=task_pool_path,
        raw_state=raw_state,
        task_pool=task_pool,
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def update_task_status(
    *,
    task_pool_path: Path,
    task_id: str,
    status: str,
    note: str | None = None,
) -> None:
    task_pool = load_json(task_pool_path, default=[])
    if not isinstance(task_pool, list):
        raise ValueError(f"Task pool must contain a JSON list: {task_pool_path}")

    for task in task_pool:
        if task.get("id") == task_id:
            task["status"] = status
            if note is not None:
                task["regulator_note"] = note
            break

    write_json(task_pool_path, task_pool)

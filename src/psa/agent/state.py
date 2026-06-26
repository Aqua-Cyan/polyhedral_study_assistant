from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from psa.coverage import coverage_manifest_path


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
    def covered_count(self) -> int:
        return int(self.summary.get("covered_records", 0))

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
    def derivations_dir(self) -> Path:
        return self.family_memory_dir / "derivations"

    @property
    def coverage_manifest_path(self) -> Path:
        return coverage_manifest_path(self.project_root, self.problem_id)

    @property    
    def final_report_path(self) -> Path:
        return self.project_root / "reports" / f"{self.problem_id}_final_report.md"

    @property
    def open_tasks(self) -> list[dict[str, Any]]:
        return [
            task
            for task in self.task_pool
            if task.get("problem_id") == self.problem_id
            and task.get("status", "open") == "open"
        ]

    def _relative_posix(self, path: Path) -> str:
        try:
            return path.relative_to(self.project_root).as_posix()
        except ValueError:
            return str(path).replace("\\", "/")

    def unverified_guess_files(self) -> list[Path]:
        """Return family guesses that do not yet have a verifier report."""
        if not self.guess_dir.exists():
            return []
        guess_files = sorted(self.guess_dir.glob("*.json"))
        unverified: list[Path] = []
        for guess_file in guess_files:
            verification_file = self.verification_dir / f"{guess_file.stem}_verification.json"
            if not verification_file.exists():
                unverified.append(guess_file)
        return unverified

    def verification_files(self) -> list[Path]:
        """All verification JSON files written by the Verifier role."""
        if not self.verification_dir.exists():
            return []
        return sorted(self.verification_dir.glob("*.json"))

    def _load_derivation_artifacts(self) -> tuple[dict[str, Path], set[str]]:
        """Return (certificates, failures) from the derivations directory.

        certificates: family_id -> certificate file path.
        failures: set of family_ids whose derivation was attempted and failed.

        A file is a certificate if it has a ``family_id`` field and its
        ``status`` is not ``failed``/``failure``. A file is a failure report
        if its ``status`` is ``failed``/``failure``. If a family has both a
        certificate and a failure report, the certificate takes precedence.
        """
        if not self.derivations_dir.exists():
            return {}, set()
        certs: dict[str, Path] = {}
        failures: set[str] = set()
        for f in sorted(self.derivations_dir.glob("*.json")):
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if not isinstance(data, dict):
                continue
            family_id = data.get("family_id")
            if not isinstance(family_id, str) or not family_id:
                continue
            status = str(data.get("status", ""))
            if status in {"failed", "failure"}:
                failures.add(family_id)
            else:
                if family_id not in certs:
                    certs[family_id] = f
        return certs, failures

    def _all_accepted_family_records(self) -> list[dict[str, Any]]:
        """All families the Verifier accepted (accept_for_implementation).

        Each record is tagged with ``has_certificate`` and
        ``derivation_failed`` so callers can split them by certificate status.
        """
        certs, failures = self._load_derivation_artifacts()
        records: list[dict[str, Any]] = []
        seen: set[str] = set()
        for vf in self.verification_files():
            try:
                vdata = json.loads(vf.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if str(vdata.get("verdict")) != "accept_for_implementation":
                continue
            guess_rel = vdata.get("guess_file")
            if not isinstance(guess_rel, str) or not guess_rel:
                continue
            guess_path = self.project_root / guess_rel
            if not guess_path.exists():
                continue
            try:
                gdata = json.loads(guess_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            family_id = str(gdata.get("family_id") or gdata.get("family_name") or "")
            if not family_id or family_id in seen:
                continue
            seen.add(family_id)
            cert_path = certs.get(family_id)
            has_cert = cert_path is not None
            derivation_failed = (family_id in failures) and not has_cert
            records.append(
                {
                    "family_id": family_id,
                    "family_name": str(gdata.get("family_name") or family_id),
                    "verification_file": self._relative_posix(vf),
                    "guess_file": str(Path(guess_rel).as_posix()),
                    "verdict": "accept_for_implementation",
                    "has_certificate": has_cert,
                    "certificate_file": self._relative_posix(cert_path) if cert_path else None,
                    "derivation_failed": derivation_failed,
                }
            )
        return records

    def accepted_family_records(self) -> list[dict[str, Any]]:
        """Families accepted by the Verifier AND carrying a derivation certificate.

        Only these families are eligible for coverage backfill, because
        recording coverage for a family without a certificate would violate
        the status-lowering rule in CLAUDE.md.
        """
        return [r for r in self._all_accepted_family_records() if r["has_certificate"]]

    def accepted_but_uncertified_records(self) -> list[dict[str, Any]]:
        """Families accepted by the Verifier but NOT yet carrying a certificate.

        These families need a DerivationProver step before they can be
        backfilled. Families whose derivation was already attempted and failed
        (a ``*_failure.json`` exists without a matching certificate) are
        excluded so the loop does not retry derivation indefinitely.
        """
        return [
            r
            for r in self._all_accepted_family_records()
            if not r["has_certificate"] and not r["derivation_failed"]
        ]


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
        json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
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

"""Persistent facet-coverage overlay for the regulator research loop.

The study adapter computes a fresh ``_state.json`` every round from a fixed
classifier. Facets that the agent later proves and records only land in
``memory/`` and were never reflected in the summary, so the stop counters
never decreased. This module supplies the missing feedback link: a
persistent coverage manifest kept under
``memory/facets/<problem>/coverage.json`` records facets that an accepted
symbolic family covers by exact normalized matching. ``apply_coverage``
overlays that manifest onto a study-adapter state dict, pruning covered
facets from the candidate/unresolved buckets and recomputing the summary
counts the regulator keys on.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping, Sequence

FACET_COVERAGE_FILENAME = "coverage.json"


def facet_key(inequality: Mapping[str, Any]) -> str:
    """Canonical string key for a normalized facet inequality."""
    coeffs = tuple(int(c) for c in inequality["coefficients"])
    rhs = int(inequality["rhs"])
    sense = str(inequality.get("sense", "<="))
    return f"c={coeffs}|r={rhs}|s={sense}"


def coverage_manifest_path(project_root: Path, problem_id: str) -> Path:
    return project_root / "memory" / "facets" / problem_id / FACET_COVERAGE_FILENAME


def _entry_key(entry: Mapping[str, Any]) -> str | None:
    inequality = entry.get("inequality")
    if isinstance(inequality, Mapping):
        try:
            return facet_key(inequality)
        except (KeyError, TypeError, ValueError):
            return None
    key = entry.get("key")
    return str(key) if key is not None else None


def load_coverage_manifest(
    project_root: Path, problem_id: str
) -> dict[str, dict[str, Any]]:
    """Load the coverage manifest written by the agent during the loop."""
    path = coverage_manifest_path(project_root, problem_id)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    if not isinstance(data, dict):
        return {}

    raw = data.get("covered", None)
    result: dict[str, dict[str, Any]] = {}

    if raw is None:
        for key, value in data.items():
            if isinstance(key, str):
                result[key] = value if isinstance(value, dict) else {"family": str(value)}
        return result

    if not isinstance(raw, list):
        return {}

    for entry in raw:
        if not isinstance(entry, dict):
            continue
        key = _entry_key(entry)
        if key is None:
            continue
        result[key] = {
            "family": entry.get("family"),
            "source": entry.get("source"),
            "note": entry.get("note"),
        }
    return result


def load_backfilled_families(project_root: Path, problem_id: str) -> set[str]:
    """Return the set of family ids already backfilled into the coverage manifest.

    The agent appends a family id to ``backfilled_families`` after it has
    recorded every covered facet for that family. The regulator uses this to
    avoid re-requesting backfill for an already-processed family, which would
    otherwise loop forever.
    """
    path = coverage_manifest_path(project_root, problem_id)
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return set()
    if not isinstance(data, dict):
        return set()
    raw = data.get("backfilled_families", [])
    if not isinstance(raw, list):
        return set()
    return {str(x) for x in raw if x}


def save_coverage_manifest(
    project_root: Path,
    problem_id: str,
    manifest: Mapping[str, Mapping[str, Any]],
    backfilled: Sequence[str] = (),
) -> None:
    """Write the manifest in the canonical shape.

    ``backfilled`` is the full list of family ids already processed. The agent
    should pass the union of the previously backfilled list and any newly
    finished family so this field never shrinks accidentally.
    """
    path = coverage_manifest_path(project_root, problem_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    covered = [
        {"key": key, "family": m.get("family"), "source": m.get("source"), "note": m.get("note")}
        for key, m in manifest.items()
    ]
    payload = {
        "problem_id": problem_id,
        "covered": covered,
        "backfilled_families": [str(f) for f in backfilled],
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def _covered_meta_for_record(
    manifest: Mapping[str, Mapping[str, Any]], record: Mapping[str, Any]
) -> tuple[str, Mapping[str, Any] | None]:
    key = facet_key(record["inequality"])
    return (key, manifest[key]) if key in manifest else (key, None)


def _relabel_covered(
    record: Mapping[str, Any], meta: Mapping[str, Any]
) -> dict[str, Any]:
    covered_record = dict(record)
    covered_record["family_status"] = "derived"
    covered_record["matched_family"] = meta.get("family")
    covered_record["derivation_status"] = "covered_by_accepted_family"
    return covered_record


def _maybe_cover_example(
    example: Mapping[str, Any], manifest: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    inequality = example.get("inequality")
    if not isinstance(inequality, Mapping):
        return dict(example)
    try:
        key = facet_key(inequality)
    except (KeyError, TypeError, ValueError):
        return dict(example)
    if key not in manifest:
        return dict(example)
    meta = manifest[key]
    covered_example = dict(example)
    covered_example["family_status"] = "derived"
    covered_example["matched_family"] = meta.get("family")
    covered_example["derivation_status"] = "covered_by_accepted_family"
    return covered_example


def _recompute_obligations(
    candidates: list[Mapping[str, Any]], unresolved: list[Mapping[str, Any]]
) -> list[str]:
    obligations: list[str] = []
    if candidates:
        obligations.append(
            "Candidate interaction facets remain. Run FamilyGuesser and "
            "DerivationProver on interaction signatures."
        )
    if unresolved:
        obligations.append(
            "Unresolved facets remain. Perform source identification, "
            "MIR-over-MIR attempts, and family compression."
        )
    if not candidates and not unresolved:
        obligations.append(
            "All currently computed facets are classified by derived or "
            "accepted families in this tested scope. A full convex-hull "
            "theorem still requires validity and reverse-inclusion proof."
        )
    return obligations


def apply_coverage(
    state: Mapping[str, Any], manifest: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    """Overlay a coverage manifest onto a study-adapter state dict."""
    if not manifest:
        return dict(state)

    manifest = dict(manifest)
    candidates = list(state.get("candidate_facets", []))
    unresolved = list(state.get("unresolved_facets", []))

    remaining_candidate: list[Mapping[str, Any]] = []
    remaining_unresolved: list[Mapping[str, Any]] = []
    covered: list[Mapping[str, Any]] = []

    for record in candidates:
        _, meta = _covered_meta_for_record(manifest, record)
        if meta is None:
            remaining_candidate.append(record)
        else:
            covered.append(_relabel_covered(record, meta))

    for record in unresolved:
        _, meta = _covered_meta_for_record(manifest, record)
        if meta is None:
            remaining_unresolved.append(record)
        else:
            covered.append(_relabel_covered(record, meta))

    groups = [dict(g) for g in state.get("facet_signature_groups", [])]
    for group in groups:
        group["examples"] = [
            _maybe_cover_example(ex, manifest) for ex in group.get("examples", [])
        ]

    summary = dict(state.get("summary", {}))
    summary["covered_records"] = len(covered)
    summary["candidate_records"] = len(remaining_candidate)
    summary["unresolved_records"] = len(remaining_unresolved)
    summary["stop_status"] = (
        "done"
        if not remaining_candidate and not remaining_unresolved
        else "continue"
    )

    new_state = dict(state)
    new_state["summary"] = summary
    new_state["candidate_facets"] = remaining_candidate
    new_state["unresolved_facets"] = remaining_unresolved
    new_state["covered_facets"] = list(covered)
    new_state["facet_signature_groups"] = groups
    new_state["proof_obligations"] = _recompute_obligations(
        remaining_candidate, remaining_unresolved
    )
    return new_state


def apply_coverage_to_state_file(
    project_root: Path, problem_id: str, state_path: Path
) -> dict[str, Any]:
    """Load manifest, overlay it onto the state file, write it back, return new state."""
    manifest = load_coverage_manifest(project_root, problem_id)
    if not manifest:
        if state_path.exists():
            return json.loads(state_path.read_text(encoding="utf-8"))
        return {}
    if not state_path.exists():
        return {}
    state = json.loads(state_path.read_text(encoding="utf-8"))
    new_state = apply_coverage(state, manifest)
    state_path.write_text(
        json.dumps(new_state, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return new_state

from __future__ import annotations

import json
from pathlib import Path

import pytest

from psa.coverage import (
    apply_coverage,
    apply_coverage_to_state_file,
    facet_key,
    save_coverage_manifest,
)


def _facet_record(coeffs, rhs, family_status="candidate", text="t", signature="s", label="L"):
    return {
        "instance": {"label": label},
        "kind": "nontrivial",
        "text": text,
        "signature": signature,
        "family_status": family_status,
        "matched_family": None,
        "derivation_status": "no_family_match",
        "inequality": {"coefficients": list(coeffs), "rhs": rhs, "sense": "<=", "support": []},
    }


def _state(candidates, unresolved, facets_total=10, derived_records=2, signature_count=3):
    groups = []
    for sig, ex in [("s1", candidates[:1]), ("s2", unresolved[:1])]:
        groups.append({"signature": sig, "count": 1, "examples": [ex], "truncated": False})
    return {
        "problem_id": "malp",
        "summary": {
            "instances": 1,
            "facets_total": facets_total,
            "derived_records": derived_records,
            "candidate_records": len(candidates),
            "unresolved_records": len(unresolved),
            "signature_count": signature_count,
            "stop_status": "continue",
        },
        "candidate_facets": list(candidates),
        "unresolved_facets": list(unresolved),
        "facet_signature_groups": groups,
        "proof_obligations": ["Candidate interaction facets remain.", "Unresolved facets remain."],
    }


def test_empty_manifest_is_identity():
    cand = [_facet_record((1, 0, 1), 1)]
    state = _state(cand, [])
    out = apply_coverage(state, {})
    assert out is not state
    assert len(out["candidate_facets"]) == 1
    assert out["summary"]["candidate_records"] == 1
    assert out["summary"]["stop_status"] == "continue"


def test_covered_candidate_is_pruned_and_relabelled():
    cand = [_facet_record((1, 0, 1), 1)]
    key = facet_key({"coefficients": (1, 0, 1), "rhs": 1, "sense": "<="})
    manifest = {key: {"family": "MyFamily", "source": "v1"}}
    out = apply_coverage(_state(cand, []), manifest)
    assert out["candidate_facets"] == []
    assert out["covered_facets"]
    assert out["covered_facets"][0]["family_status"] == "derived"
    assert out["covered_facets"][0]["matched_family"] == "MyFamily"
    assert out["summary"]["candidate_records"] == 0
    assert out["summary"]["unresolved_records"] == 0
    assert out["summary"]["covered_records"] == 1
    assert out["summary"]["stop_status"] == "done"
    assert out["proof_obligations"] == ["All currently computed facets are classified by derived or "
                                       "accepted families in this tested scope. A full convex-hull "
                                       "theorem still requires validity and reverse-inclusion proof."]


def test_covered_unresolved_is_pruned():
    unres = [_facet_record((0, 1, 0), 0, family_status="unresolved")]
    key = facet_key({"coefficients": (0, 1, 0), "rhs": 0, "sense": "<="})
    out = apply_coverage(_state([], unres), {key: {"family": "F"}})
    assert out["unresolved_facets"] == []
    assert out["covered_facets"]
    assert out["summary"]["stop_status"] == "done"


def test_partial_coverage_keeps_loop_running():
    cand1 = _facet_record((1, 0, 1), 1)
    cand2 = _facet_record((0, 1, 1), 1)
    key = facet_key({"coefficients": (1, 0, 1), "rhs": 1, "sense": "<="})
    out = apply_coverage(_state([cand1, cand2], []), {key: {"family": "F"}})
    assert len(out["candidate_facets"]) == 1
    assert out["summary"]["candidate_records"] == 1
    assert out["summary"]["stop_status"] == "continue"


def test_idempotent():
    cand = [_facet_record((1, 0, 1), 1)]
    key = facet_key({"coefficients": (1, 0, 1), "rhs": 1, "sense": "<="})
    manifest = {key: {"family": "F"}}
    once = apply_coverage(_state(cand, []), manifest)
    twice = apply_coverage(once, manifest)
    assert twice["candidate_facets"] == once["candidate_facets"]
    assert twice["covered_facets"] == once["covered_facets"]
    assert twice["summary"] == once["summary"]


def test_apply_coverage_to_state_file_roundtrip(tmp_path: Path):
    problem_id = "malp"
    facet = {"coefficients": [1, 0, 1], "rhs": 1, "sense": "<=", "support": []}
    state = _state([_facet_record((1, 0, 1), 1)], [])
    state_path = tmp_path / "reports" / f"{problem_id}_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state), encoding="utf-8")

    # no manifest yet -> unchanged
    apply_coverage_to_state_file(tmp_path, problem_id, state_path)
    loaded = json.loads(state_path.read_text(encoding="utf-8"))
    assert loaded["summary"]["candidate_records"] == 1
    assert loaded["summary"]["stop_status"] == "continue"

    # write manifest then overlay
    manifest = {facet_key(facet): {"family": "F", "source": "v1"}}
    save_coverage_manifest(tmp_path, problem_id, manifest)
    apply_coverage_to_state_file(tmp_path, problem_id, state_path)
    loaded = json.loads(state_path.read_text(encoding="utf-8"))
    assert loaded["summary"]["candidate_records"] == 0
    assert loaded["summary"]["covered_records"] == 1
    assert loaded["summary"]["stop_status"] == "done"

from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("cdd")

from examples.malp.study import run


def test_malp_study_smoke() -> None:
    state = run(max_union_size=1)

    assert state["problem_id"] == "malp"
    assert "summary" in state
    assert "candidate_records" in state["summary"]
    assert Path("reports/malp_state.json").exists()
    assert Path("reports/malp_report.md").exists()

    loaded = json.loads(Path("reports/malp_state.json").read_text(encoding="utf-8"))
    assert loaded["problem_id"] == "malp"
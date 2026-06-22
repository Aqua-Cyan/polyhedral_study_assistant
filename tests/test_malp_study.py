from pathlib import Path

import pytest

pytest.importorskip("cdd")

from examples.malp.study import run_study


def test_malp_study_smoke(tmp_path: Path) -> None:
    outputs = run_study(tmp_path)

    assert outputs.report_path.exists()
    assert outputs.json_path.exists()
    assert "## Derived or proved symbolic inequality families" in outputs.report_text
    assert "## Candidate symbolic inequality families" in outputs.report_text
    assert "## Derivation attempts for not-yet-covered facets" in outputs.report_text
    assert "## Unresolved computed facets" in outputs.report_text

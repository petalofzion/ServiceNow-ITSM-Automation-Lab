from pathlib import Path

from scripts.sn_apply_desired_state import build_plan_text


def test_plan_matches_snapshot() -> None:
    desired_state_dir = Path("ops/desired-state")
    plan_text = build_plan_text(desired_state_dir)
    snapshot = Path("tests/fixtures/desired_state_plan.txt").read_text()
    assert plan_text == snapshot

# Test Playbook (ATF + Validation)

## Goal
Run ATF suites and scripted validations against the automated build.

## Steps
1. Trigger ATF suite run.
   - Run: `python scripts/sn_run_atf.py --suite "Plego ITSM Regression"`
2. Validate critical records with scripted checks.
   - Run: `python scripts/sn_apply_desired_state.py --verify`
3. Record ATF run IDs in `docs/success-metrics.md`.

## Expected outputs
- ATF run results stored in `artifacts/atf_runs/`.
- Validation report stored in `artifacts/exports/`.

# Export Playbook (Artifacts + Evidence)

## Goal
Export update sets, app packages, and evidence artifacts for reproducibility.

## Steps
1. Export artifacts.
   - Run: `python scripts/sn_export_artifacts.py`
2. Capture evidence (screenshots, logs).
   - Run: `python scripts/sn_capture_evidence.py`
3. Attach outputs to PR or store in `artifacts/`.

## Expected outputs
- Update sets and app packages in `artifacts/exports/`.
- Screenshots and evidence in `artifacts/screenshots/`.

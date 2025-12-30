# Build Playbook (Automation-First)

## Goal
Converge a ServiceNow PDI to the desired state defined in `ops/desired-state/` without manual UI steps.

## Prerequisites
- ServiceNow MCP server available (local or CI-side).
- ServiceNow credentials configured as environment variables or secrets.
- Python 3.11+.

## Steps
1. Validate desired state files.
   - Run: `python scripts/sn_apply_desired_state.py --validate`
2. Apply desired state.
   - Run: `python scripts/sn_apply_desired_state.py --apply`
3. Seed data for flows, PA, and integrations.
   - Run: `python scripts/sn_seed_data.py`
4. Capture evidence (optional).
   - Run: `python scripts/sn_capture_evidence.py`

## Expected outputs
- Updated ServiceNow instance aligned with the YAML desired state.
- Evidence artifacts logged in `docs/success-metrics.md` and `artifacts/`.

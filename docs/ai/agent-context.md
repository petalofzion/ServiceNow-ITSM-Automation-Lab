# AI Agent Context

## Mission
Execute the build of the ServiceNow ITSM Automation Lab in a PDI using the documentation in this repo. Record evidence and update the success metrics as you go.

## Source of truth
- Scope, architecture, and requirements: `docs/spec-architecture-requirements.md`
- Execution steps: `docs/ai/autonomous-workflows.md`
- Evidence tracking: `docs/success-metrics.md`

## Working assumptions
- PDI is available and accessible.
- You have admin access in the PDI.
- You can create scoped apps, tables, and scripts.

## Conventions
- Use the `x_plego` app scope prefix.
- Name tables with `u_plego_*`.
- Log all integration calls in `u_plego_integration_log`.

## Evidence capture checklist
- Screenshot each major configuration screen.
- Export reports (PDF/CSV) for KPI evidence.
- Capture a before/after performance optimization comparison.

## Definition of done
All requirements are satisfied, evidence is captured, and `docs/success-metrics.md` is up to date.

# ServiceNow ITSM Automation Lab
Catalog → Flow Designer → Integrations → Analytics

This repository scaffolds a complete, resume-ready ServiceNow ITSM automation lab. It is intentionally automation-first so agents can converge a Personal Developer Instance (PDI) to the desired state without manual UI steps while keeping evidence of progress, decisions, and outcomes.

## What you will build
A scoped ServiceNow app named **Plego ITSM Automation Lab** that implements an end-to-end request lifecycle:
- Service Catalog + Record Producer
- Flow Designer approvals, SLAs, and notifications
- Performance Analytics dashboards
- REST/SOAP integrations (MID Server best-effort)
- Security/ITIL alignment
- Performance tuning + operational logging

## Repository map
- `docs/spec-architecture-requirements.md` — single source of truth for scope, architecture, and requirements
- `docs/success-metrics.md` — success metrics tracker for resume-ready proof
- `docs/ai/agent-context.md` — AI agent context and environment setup
- `docs/ai/autonomous-workflows.md` — automation playbooks for agent-driven builds
- `docs/testing-ci.md` — ATF suites and CI gates
- `docs/servicenow/atf-test-blueprints.md` — detailed ATF test steps
- `docs/ci/github-actions.md` — CI/CD guidance for ServiceNow ATF
- `docs/implementation/` — detailed build instructions and checklists
- `docs/servicenow/` — configuration blueprints per module
- `src/` — template library (Script Includes, Business Rules, etc.) with TODO comments
- `ops/desired-state/` — declarative desired state the agent converges to
- `ops/playbooks/` — build/test/export orchestration guides
- `scripts/` — automation entrypoints calling MCP/SN APIs
- `.github/workflows/` — CI checks and ServiceNow orchestration workflows
- `artifacts/` — generated exports, ATF runs, and evidence

## How to use
1. Start in `docs/spec-architecture-requirements.md` to understand scope.
2. Follow `docs/ai/autonomous-workflows.md` to execute the build automation.
3. Use `docs/success-metrics.md` to log progress and evidence (screenshots, links, metrics).
4. Set up ATF suites using `docs/implementation/atf-setup.md`.
5. Follow `CHECKLIST.md` before merging any change.

## Testing + CI gates
- ATF suites are documented in `docs/testing-ci.md` and `docs/servicenow/atf-test-blueprints.md`.
- CI guidance and example workflow live in `docs/ci/github-actions.md` and `docs/ci/github-actions-example.yml`.
- Failure handling steps are in `CI_FAIL_PLAYBOOK.md`.

## Status
This is a scaffold. All ServiceNow configurations are to be converged automatically from the desired state and playbooks.

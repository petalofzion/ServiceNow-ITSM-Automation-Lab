# Autonomous Workflows (AI Execution Playbooks)

These playbooks are designed for AI agents to execute the build end-to-end. Follow in order.

## Workflow 1 — Initialize app + data model
1. Create scoped app: **Plego ITSM Automation Lab** (`x_plego`).
2. Create tables:
   - `u_plego_request`
   - `u_plego_asset`
   - `u_plego_integration_log`
3. Add essential fields per `docs/servicenow/data-model.md`.
4. Update `docs/success-metrics.md` with evidence links.

## Workflow 2 — Catalog + record producer
1. Create catalog items:
   - Access Request
   - New Laptop Request
2. Create record producer:
   - Report an Incident (creates Incident + links to request)
3. Configure UI policies and client scripts from `src/ui_policies/` and `src/client_scripts/`.
4. Capture screenshots of the forms.

## Workflow 3 — Flow Designer and automation
1. Build flow for approvals (manager → IT), auto-assign, SLA timers.
2. Add notifications and state transitions.
3. Validate via test requests; log results.

## Workflow 4 — Scripting + policy
1. Implement business rules from `src/business_rules/`.
2. Implement script includes + GlideAjax from `src/script_includes/`.
3. Confirm server/client scripts enforce policy rules.

## Workflow 5 — Analytics + dashboards
1. Define KPIs and indicators (cycle time, SLA met %, requests by category/group).
2. Build dashboard and add filters.
3. Schedule report export.
4. Add evidence to success metrics.

## Workflow 6 — Integrations
1. Outbound REST: create GitHub issue on high-priority approval.
2. Inbound REST API: create/update request.
3. SOAP call: store response in integration log.
4. MID Server: attempt setup or follow stub in `docs/servicenow/integrations.md`.

## Workflow 7 — Performance + troubleshooting
1. Create intentional inefficient query.
2. Optimize with index + improved GlideRecord queries + caching.
3. Document before/after in `docs/servicenow/performance.md`.

## Workflow 8 — Security + ITIL alignment
1. Create roles and ACLs.
2. Lock down sensitive fields.
3. Ensure audit trails and ITIL-aligned flows.

## Workflow 9 — Evidence mapping
1. Map deliverables to job bullets in `docs/evidence-map.md`.
2. Final review of success metrics.

## Workflow 10 — Testing + CI readiness
1. Build ATF suites using `docs/implementation/atf-setup.md`.
2. Implement tests per `docs/servicenow/atf-test-blueprints.md`.
3. Record ATF run IDs and results in `docs/success-metrics.md`.
4. Follow `CHECKLIST.md` and `CI_FAIL_PLAYBOOK.md` for gatekeeping.

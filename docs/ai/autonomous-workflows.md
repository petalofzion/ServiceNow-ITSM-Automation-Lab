# Autonomous Workflows (AI Execution Playbooks)

These playbooks are designed for AI agents to execute the build end-to-end using automation tools. Follow in order.

## Workflow 1 — Initialize app + data model
1. Validate desired state files in `ops/desired-state/`.
2. Apply desired state via `scripts/sn_apply_desired_state.py`.
3. Confirm tables and fields align with `docs/servicenow/data-model.md`.
4. Update `docs/success-metrics.md` with evidence links.

## Workflow 2 — Catalog + record producer
1. Apply catalog definitions from `ops/desired-state/catalog.yml`.
2. Deploy UI policies and client scripts from `src/ui_policies/` and `src/client_scripts/`.
3. Capture evidence via `scripts/sn_capture_evidence.py`.

## Workflow 3 — Flow Designer and automation
1. Apply flow definitions from `ops/desired-state/flows.yml`.
2. Validate via seeded requests from `scripts/sn_seed_data.py`.
3. Log results in `docs/success-metrics.md`.

## Workflow 4 — Scripting + policy
1. Implement business rules from `src/business_rules/`.
2. Implement script includes + GlideAjax from `src/script_includes/`.
3. Confirm server/client scripts enforce policy rules via validation checks.

## Workflow 5 — Analytics + dashboards
1. Apply dashboard definitions from `ops/desired-state/pa_dashboards.yml`.
2. Seed KPI data with `scripts/sn_seed_data.py`.
3. Export reports using `scripts/sn_export_artifacts.py`.
4. Add evidence to success metrics.

## Workflow 6 — Integrations
1. Apply integration definitions from `ops/desired-state/integrations.yml`.
2. Trigger outbound REST flow via seeded high-priority records.
3. Validate inbound REST API with scripted checks.
4. MID Server: attempt setup or follow stub in `docs/servicenow/integrations.md`.

## Workflow 7 — Performance + troubleshooting
1. Create intentional inefficient query.
2. Optimize with index + improved GlideRecord queries + caching.
3. Document before/after in `docs/servicenow/performance.md`.

## Workflow 8 — Security + ITIL alignment
1. Apply roles and ACLs from `ops/desired-state/roles_acls.yml`.
2. Lock down sensitive fields via scripts and policies.
3. Ensure audit trails and ITIL-aligned flows.

## Workflow 9 — Evidence mapping
1. Map deliverables to job bullets in `docs/evidence-map.md`.
2. Final review of success metrics.

## Workflow 10 — Testing + CI readiness
1. Build ATF suites using `docs/implementation/atf-setup.md`.
2. Implement tests per `docs/servicenow/atf-test-blueprints.md`.
3. Trigger ATF with `scripts/sn_run_atf.py`.
4. Record ATF run IDs and results in `docs/success-metrics.md`.
5. Follow `CHECKLIST.md` and `CI_FAIL_PLAYBOOK.md` for gatekeeping.

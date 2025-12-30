# Implementation Acceptance Checklist (Automation-First)

## Phase 1 — Setup (Converge Desired State)
- [ ] Run `make build` to converge the instance.
- [ ] Validate tables and fields align with `docs/servicenow/data-model.md`.
- [ ] Validate roles and ACLs match `ops/desired-state/roles_acls.yml`.

## Phase 2 — Catalog + Flows (Automated)
- [ ] Validate catalog items in `ops/desired-state/catalog.yml` exist in the instance.
- [ ] Validate record producer exists and is wired to flows in `ops/desired-state/flows.yml`.
- [ ] Run seeded requests via `scripts/sn_seed_data.py` and verify outcomes.

## Phase 3 — Scripting (Template Library)
- [ ] Validate Business Rules from `src/business_rules/` are applied by automation.
- [ ] Validate Script Includes + GlideAjax from `src/script_includes/`.
- [ ] Validate Client Scripts + UI Policies from `src/client_scripts/` and `src/ui_policies/`.

## Phase 4 — Analytics (Automated)
- [ ] Validate KPI/indicator definitions from `ops/desired-state/pa_dashboards.yml`.
- [ ] Seed data via `scripts/sn_seed_data.py`.
- [ ] Export reports via `scripts/sn_export_artifacts.py`.

## Phase 5 — Integrations (Automated)
- [ ] Validate REST/SOAP definitions from `ops/desired-state/integrations.yml`.
- [ ] Trigger outbound REST flow via seeded records and verify logs.
- [ ] Validate inbound REST API with scripted checks.
- [ ] MID Server: confirm automated setup or document stub in `docs/servicenow/integrations.md`.

## Phase 6 — Performance + Stability (Automated)
- [ ] Apply baseline inefficient rule via automation.
- [ ] Apply optimized version and document before/after in `docs/servicenow/performance.md`.
- [ ] Validate operational logging entries exist.

## Phase 7 — Evidence (Automated + Logged)
- [ ] Update `docs/success-metrics.md` with links to exports and ATF runs.
- [ ] Capture evidence via `scripts/sn_capture_evidence.py` when supported.
- [ ] Ensure `/artifacts` contains exports, ATF runs, and screenshots.

## Phase 8 — Testing + CI (Automated)
- [ ] Run `make test` to execute ATF suites.
- [ ] Validate tests per `docs/servicenow/atf-test-blueprints.md`.
- [ ] Run `make export` to capture artifacts and evidence.
- [ ] Follow `CHECKLIST.md` before merge.

# Step-by-Step Implementation Checklist

## Phase 1 — Setup
- [ ] Create scoped app `Plego ITSM Automation Lab`.
- [ ] Create tables per `docs/servicenow/data-model.md`.
- [ ] Add roles and ACLs.

## Phase 2 — Catalog + Flows
- [ ] Create Access Request and New Laptop Request.
- [ ] Create Record Producer: Report an Incident.
- [ ] Build Flow Designer process.

## Phase 3 — Scripting
- [ ] Implement Business Rules.
- [ ] Implement Script Includes + GlideAjax.
- [ ] Implement Client Scripts + UI Policies.

## Phase 4 — Analytics
- [ ] Create KPIs and indicators.
- [ ] Build dashboard with filters.
- [ ] Schedule report export.

## Phase 5 — Integrations
- [ ] Outbound REST call.
- [ ] Inbound REST API.
- [ ] SOAP call.
- [ ] MID Server best-effort or stub.

## Phase 6 — Performance + Stability
- [ ] Implement inefficient rule.
- [ ] Optimize and document before/after.
- [ ] Add operational logging.

## Phase 7 — Evidence
- [ ] Update `docs/success-metrics.md`.
- [ ] Capture screenshots and logs.
- [ ] Finalize demo script.

## Phase 8 — Testing + CI
- [ ] Build ATF suites per `docs/implementation/atf-setup.md`.
- [ ] Implement tests per `docs/servicenow/atf-test-blueprints.md`.
- [ ] Follow `CHECKLIST.md` before merge.

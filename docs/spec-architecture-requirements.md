# Spec + Architecture + Requirements

## Core idea (one sentence)
Build a scoped ServiceNow app in a Personal Developer Instance (PDI) that implements an end-to-end IT request lifecycle: Service Catalog + Record Producer → approvals/workflows → dashboards/Performance Analytics → integrations (REST/SOAP, MID Server if possible) → security/ITIL alignment → performance tuning + stability.

## Architecture overview
**Runtime:** ServiceNow PDI (scoped app: `Plego ITSM Automation Lab`)

**Primary components**
- **Data model:** custom tables for requests, assets, and integration logs.
- **Catalog:** Access Request + New Laptop Request.
- **Record Producer:** Report an Incident (creates Incident + links to request).
- **Flow Designer:** approvals, SLAs, notifications, state transitions.
- **Scripting:** business rules, UI policies, client scripts, script includes, GlideAjax.
- **Analytics:** Performance Analytics KPIs + dashboards + scheduled reports.
- **Integrations:** outbound REST, inbound REST API, SOAP call, MID Server (best-effort).
- **Security:** roles + ACLs + credential handling + ITIL-ish controls.
- **Operations:** logging, troubleshooting guides, performance tuning exercise.

### Logical flow
1. User submits catalog item or record producer.
2. Flow routes approvals, sets SLAs, updates state, notifies stakeholders.
3. Integrations triggered on high-priority approvals; responses logged.
4. KPIs and dashboards track throughput, cycle time, SLA compliance.
5. Security and audit trail prove ITIL alignment.

## Requirements
### Functional requirements
1. **Scoped app + modules**
   - App: `Plego ITSM Automation Lab`
   - Tables: `u_plego_request`, `u_plego_asset`, `u_plego_integration_log`
2. **Catalog + record producers + workflow**
   - Catalog Items: Access Request, New Laptop Request
   - Record Producer: Report an Incident
   - Flow: auto-assign, approvals (manager → IT), SLAs, notifications, state transitions
3. **Scripting + policy**
   - UI policies: dynamic field behavior
   - Client scripts: validation + dynamic population
   - Business rules: enforce state transitions + data integrity
   - Script includes: utilities + GlideAjax + policy helpers
4. **Performance Analytics**
   - KPIs: cycle time, SLA met %, requests by category/assignment group
   - Dashboard with filters + scheduled exports
5. **Integrations**
   - Outbound REST (RESTMessageV2) + log to `u_plego_integration_log`
   - Inbound REST API (token auth)
   - SOAP call to public endpoint (or mock)
   - MID Server best-effort or documented stub
6. **Troubleshooting + performance**
   - One inefficient query + optimized version
   - Operational logging and error handling
   - Debugging guide
7. **Security + ITIL alignment**
   - Roles: `x_plego.user`, `x_plego.it_agent`, `x_plego.admin`
   - ACLs for sensitive fields
   - Credential store usage (or protected system properties)
   - ITIL patterns: approvals, SLAs, audit trail

### Non-functional requirements
- Documented, repeatable steps for AI agents.
- Minimal code stubs with TODOs for each major script area.
- Evidence trail for resume-ready demonstration.

## Acceptance criteria
- All deliverables are fully configured in PDI and documented.
- At least one high-priority request triggers outbound REST integration.
- Inbound REST API can create/update a request.
- SOAP call returns and stores a response.
- Dashboard includes KPIs and filters.
- Performance optimization includes before/after documentation.

## Out of scope (for now)
- Production hardening, HA, and enterprise-scale security configurations.
- Advanced ITOM/HRSD/SecOps beyond ITSM.

## Risks + mitigations
- **MID Server setup fails locally:** document “MID Server–ready” design and stub.
- **Integration endpoints unavailable:** use mock or public test endpoints; record exact steps.
- **Performance Analytics access limitations:** use reports + mock PA screenshots if needed.

## Deliverables
- Docs + scripts in this repo.
- Configurations in PDI following the docs.
- Evidence screenshots and metrics captured in `docs/success-metrics.md`.

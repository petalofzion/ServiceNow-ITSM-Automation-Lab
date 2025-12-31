# Tests + CI Gates (ATF)

This project uses ServiceNow Automated Test Framework (ATF) as the primary test harness. These suites are designed to keep the implementation stable while iterating.

Test suite intent, schedules, and responsibility mapping live in `docs/testing/test-taxonomy.md`.

## ATF Suites to create in the PDI
### 1) Smoke Suite (runs fast on every change)
- **Create Catalog Request (Access Request)**
  - Fill variables → submit → verify Request + RITM created.
- **Approval Path**
  - Set up manager approver → approve → verify state transitions.
- **Assignment + SLA**
  - Verify assignment group set and SLA fields populated (or timers started).
- **Security sanity**
  - User without `x_plego.it_agent` role cannot edit protected fields (ACL test).
- **Dashboard sanity**
  - Create 3 sample records → verify report widget returns non-zero counts.

### 2) Regression Suite (runs nightly or before release)
- Record Producer creates Incident correctly and links to request.
- UI Policies hide/show correctly based on category/urgency.
- Business Rules prevent invalid transitions.
- Script Include functions return expected outputs.
- Data quality: no orphaned records, required fields always set.

### 3) Integration Suite (mocked where possible)
- Outbound REST: verify payload formed and response logged.
- Inbound REST: scripted REST API accepts valid request, rejects invalid.
- SOAP call: returns parsed fields and stores response.
- If real third-party calls are flaky, mock them to keep CI green.

## Workflow gates
- **On PR:** run Smoke Suite.
- **On main merge:** run Smoke + Integration.
- **Nightly:** run full Regression.

## Definition-of-done gate for AI agents
Before merging any change, provide evidence of:
- ATF Smoke Suite pass.
- No new errors in system logs during test run.
- Integration calls passing or mocked (no flaky network dependence).
- ACL test still passes (unauthorized user blocked).
- Dashboard sanity test still passes.

## Repo-side test gates (non-ATF)
- `make validate`: desired state schema validation.
- Idempotency: apply desired state twice; second run must be no-op.
- Drift detection: compare instance artifacts vs `ops/desired-state/`.
- Evidence pack validation: ATF run JSON + artifacts exist after `make test`.
- Security scans: gitleaks + dependency audit + static analysis.

## CI pipeline option (recommended)
Use GitHub Actions to trigger ServiceNow CI/CD “Run ATF Test Suite”.
- PR: Smoke suite
- Merge to main: Smoke + Integration
- Nightly: Regression

**Note:** Store instance URL and credentials in GitHub Actions secrets. Use ServiceNow CI/CD integrations where available.

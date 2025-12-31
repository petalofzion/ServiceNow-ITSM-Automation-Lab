# Test Taxonomy

This document defines the test suites, their intent, when they run, and how they map
to job responsibilities. These suites are created and managed by automation.

## Suites

### Smoke
- Purpose: Validate the core request lifecycle end-to-end with minimal scope.
- Runs: every PR / every change.
- Coverage:
  - Catalog submit works (request + RITM).
  - Record producer creates incident.
  - Flow runs and approval path advances state.
  - Script include logging produces a trace record.
  - ACL sanity for requester vs IT agent.
 - ATF tests:
   - Catalog Access Request Submission (sys_id: 1e801603538afe10fd7b7bd0a0490e33)
   - Record Producer Creates Incident (sys_id: 4e629647538afe10fd7b7bd0a0490e50)
   - Access Request Flow Trigger (sys_id: ee629647538afe10fd7b7bd0a0490eed)
   - Access Request Approval Path (sys_id: d0c9d09f538a3250fd7b7bd0a0490e9b)
   - Smoke Logging and Script Includes (sys_id: 3cc9149f538a3250fd7b7bd0a0490e4f)
   - ACL Sanity Checks (sys_id: c5c9149f538a3250fd7b7bd0a0490ebc)

### Integration
- Purpose: Prove outbound/inbound REST + SOAP logging and error handling.
- Runs: merge to main and nightly.
- Coverage:
  - Outbound REST success + log.
  - Outbound REST failure handling + log.
  - Inbound REST creates request and enforces auth.
  - SOAP call parsed + logged.
- ATF tests:
   - Outbound REST Success (sys_id: d1c9149f538a3250fd7b7bd0a0490ef6)
   - Outbound REST Failure Handling (sys_id: a5c9549f538a3250fd7b7bd0a0490e3c)
   - Inbound REST Creates Request (sys_id: 8ec9549f538a3250fd7b7bd0a0490e8e)
   - SOAP Call Logged (sys_id: 5ac9949f538a3250fd7b7bd0a0490e38)

### Regression
- Purpose: Protect edge cases and long-lived stability.
- Runs: nightly or before release.
- Coverage:
  - UI policy + client script correctness.
  - State transition guards.
  - SLA/timer behavior.
  - Dashboard/report sanity with seeded data.
 - ATF tests (to be created):
   - UI Policies Behavior (sys_id: TBD)
   - State Guard Validation (sys_id: TBD)
   - SLA/TIMER Sanity (sys_id: TBD)
   - Dashboard Widget Counts (sys_id: TBD)

### Performance & Stability
- Purpose: Prove stability + performance guardrails.
- Runs: weekly or manual release gate.
- Coverage:
  - Baseline runtime + error log check.
  - Optimized query verification.
  - System log health (no errors during run).
- ATF tests (to be created):
  - Performance Baseline (sys_id: TBD)
  - Optimized Query Check (sys_id: TBD)
  - Error Log Sweep (sys_id: TBD)

## CI gates
- PR: Smoke
- Merge to main: Smoke + Integration
- Nightly: Regression

## Responsibility mapping
| Responsibility | Suite | Test IDs |
|---|---|---|
| Catalog + request workflows | Smoke | 1e801603538afe10fd7b7bd0a0490e33 |
| Record producers | Smoke | 4e629647538afe10fd7b7bd0a0490e50 |
| Flow Designer + approvals | Smoke | ee629647538afe10fd7b7bd0a0490eed, d0c9d09f538a3250fd7b7bd0a0490e9b |
| REST/SOAP integrations | Integration | d1c9149f538a3250fd7b7bd0a0490ef6, a5c9549f538a3250fd7b7bd0a0490e3c, 8ec9549f538a3250fd7b7bd0a0490e8e, 5ac9949f538a3250fd7b7bd0a0490e38 |
| Security/ACLs | Smoke + Regression | c5c9149f538a3250fd7b7bd0a0490ebc |
| Dashboards/analytics | Regression | TBD |
| Performance/stability | Performance & Stability | TBD |

## Repo-side test suite (non-ATF)
- Desired state schema validation: `make validate`.
- Idempotency check: apply desired state twice; second run must be no-op.
- Drift detection: compare instance artifacts vs `ops/desired-state/`.
- Evidence pack validation: ATF run JSON + artifact exports exist after `make test`.
- Security scans: secrets (gitleaks), dependency audit (pip-audit/npm audit), lint (ruff/bandit).

## Notes
- ATF run API is not available in this PDI; suites must be run manually in the UI.

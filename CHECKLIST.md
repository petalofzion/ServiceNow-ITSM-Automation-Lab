# CHECKLIST (Agent Run Requirements)

Use this checklist before merging any change.

## Required checks
- [ ] Run ATF Smoke Suite in ServiceNow.
- [ ] Confirm no new errors in system logs during test run.
- [ ] Confirm integrations are passing or mocked (no flaky network dependence).
- [ ] Confirm ACL test passes (unauthorized user blocked).
- [ ] Confirm dashboard sanity test passes.

## When behavior changes
- [ ] Update README with new run steps.
- [ ] Update docs/testing-ci.md if suite or gate changes.

## Evidence to capture
- [ ] ATF run ID(s).
- [ ] Screenshot of failed step if any.
- [ ] Summary in `docs/success-metrics.md`.

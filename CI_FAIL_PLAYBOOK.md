# CI Failure Playbook

Use this playbook to respond to failed checks consistently.

## If ATF fails
- Record the ATF run ID.
- Capture a screenshot of the failing step.
- Check system logs for new errors and include relevant excerpts.
- Update `docs/success-metrics.md` with the failure and resolution plan.

## If lint fails
- Run the formatter or lint auto-fix configured for the repo.
- Re-run the failing check and note the outcome.

## If golden dataset changes
- Explain why the data changed.
- Update expected outputs or fixtures accordingly.
- Capture before/after evidence if relevant.

## If a REST/SOAP integration test fails
- Verify credentials and endpoint availability.
- If external dependency is flaky, switch to mock and document the change.
- Re-run Integration Suite and note any changes.

## If ACL/security test fails
- Review role assignments and ACL rules.
- Verify protected fields are scoped to `x_plego.it_agent` / `x_plego.admin`.
- Re-run Smoke Suite.

## If dashboard sanity fails
- Verify sample data creation steps.
- Rebuild or refresh the report widget.
- Re-run Smoke Suite.

## If business rule or script include test fails
- Validate GlideRecord queries and guard conditions.
- Ensure script include signature matches the tests.
- Add or update logging for debugging.

# ATF Test Blueprints

These are detailed step outlines to build each Automated Test Framework (ATF) test in the PDI.

## Smoke Suite
### Test: Create Catalog Request (Access Request)
1. Open Catalog Item: Access Request.
2. Fill variables (requested_for, system, access level, urgency, justification).
3. Submit request.
4. Assert Request (`u_plego_request`) and RITM exist.

### Test: Approval Path
1. Create request with a known manager.
2. Approve as manager.
3. Approve as IT agent.
4. Verify state transitions: New → Awaiting Approval → In Progress.

### Test: Assignment + SLA
1. Create request with known category/urgency.
2. Verify assignment group is set.
3. Verify SLA timer fields populated or SLA attached.

### Test: Security sanity
1. Impersonate user without `x_plego.it_agent`.
2. Attempt to edit protected field.
3. Assert update blocked by ACL.

### Test: Dashboard sanity
1. Create 3 sample `u_plego_request` records.
2. Load report widget.
3. Assert non-zero counts in widget output.

## Regression Suite
### Test: Record Producer creates Incident
1. Open Record Producer: Report an Incident.
2. Submit with required fields.
3. Assert Incident created and linked to `u_plego_request`.

### Test: UI Policies
1. Open Access Request item.
2. Set urgency/category to trigger UI policy.
3. Assert fields show/hide correctly.

### Test: Business Rules state guard
1. Attempt invalid state transition.
2. Assert update blocked and user message shown.

### Test: Script Include outputs
1. Call `PlegoUtils.getAssignmentGroup` with sample inputs.
2. Assert returned group matches expected sys_id.

### Test: Data quality
1. Query for requests where both `requested_item` and `incident` are empty.
2. Assert none returned.
3. Query for requests where both `requested_item` and `incident` are populated.
4. Assert none returned (each request should link to exactly one of the two).

## Integration Suite
### Test: Outbound REST (mocked)
1. Trigger high-priority approval.
2. Use mock endpoint.
3. Assert request payload stored in `u_plego_integration_log`.

### Test: Inbound REST
1. POST valid payload to scripted REST API.
2. Assert request created.
3. POST invalid payload → assert error response.

### Test: SOAP call
1. Run SOAP action.
2. Assert parsed fields stored in `u_plego_integration_log`.

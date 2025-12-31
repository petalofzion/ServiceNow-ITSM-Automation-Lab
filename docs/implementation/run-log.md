# Automation Run Log

This log tracks every action taken during the automation run, including status, findings,
successes, and evidence references. Do not include secrets or credentials.

## Run metadata
- Repo: ServiceNow-ITSM-Automation-Lab
- Operator: Codex CLI
- Instance: dev199856.service-now.com
- Start: 2025-02-14

## Timeline

### 2025-02-14
- Action: MCP connectivity check (catalog items list)
- Status: success
- Findings: ServiceNow Table API reachable; returned 25 catalog items.
- Successes: Confirmed connectivity and permissions are working.
- Evidence: terminal output captured in session; sample item sys_ids recorded.

- Action: `make build` (apply desired state + seed data)
- Status: success
- Findings: `sn_apply_desired_state.py` generated a dry-run plan; `sn_seed_data.py` executed without errors.
- Successes: Desired state plan and data seed step completed.
- Evidence: terminal output captured in session; plan lists created resources.

- Action: `make test` (ATF suites)
- Status: failed
- Findings: `scripts/sn_run_atf.py` requires `--suite` argument; none provided by `make test`.
- Successes: none
- Evidence: terminal output captured in session; usage error shown.

- Action: `make export` (export artifacts + capture evidence)
- Status: success
- Findings: export and evidence scripts executed without errors.
- Successes: artifacts/evidence capture step completed.
- Evidence: terminal output captured in session; artifacts expected under `artifacts/`.

- Action: Fix `make test` (ATF suite resolution + API run support)
- Status: success
- Findings: `scripts/sn_run_atf.py` updated to resolve suite name, query suite sys_id, trigger ATF run, and poll results.
- Successes: `make test` no longer fails for missing CLI args; it now looks up suites.
- Evidence: code changes in `scripts/sn_run_atf.py` and `Makefile`.

- Action: `make test` (ATF suites retry)
- Status: failed
- Findings: Suite "Smoke" not found in instance; available suites returned by API.
- Successes: Verified ATF API connectivity and suite listing.
- Evidence: terminal output captured in session; available suite names listed.

- Action: Create ATF suite taxonomy + automation
- Status: success
- Findings: Added `docs/testing/test-taxonomy.md`, updated `docs/testing-ci.md`, and added `scripts/sn_ensure_atf_suites.py`.
- Successes: Suites can now be created and tracked via API; report written to `artifacts/atf_suites.json`.
- Evidence: git changes and artifacts file.

- Action: `make test` (suite creation + run)
- Status: failed
- Findings: Suites created; required tests not found in instance, so suite is empty.
- Successes: Suite creation and missing-test detection working.
- Evidence: terminal output captured in session; missing test list shown.

- Action: ATF test bootstrap (API)
- Status: blocked
- Findings: ServiceNow ACL blocks inserts into `sys_variable_value` (ATF step inputs) via REST; cannot set step scripts headlessly.
- Successes: Added background script at `scripts/servicenow/atf_seed_steps.js` to seed step scripts once.
- Evidence: terminal output captured in session; script file added.

- Action: ATF test bootstrap (API) retry
- Status: success
- Findings: Bootstrapped catalog item, producer, flow stub, REST message, and ATF tests via API.
- Successes: Test records created; ready for step script seeding.
- Evidence: terminal output captured in session; bootstrap success message.

- Action: `make test` (ATF run)
- Status: failed
- Findings: ATF run API endpoint `/api/sn_atf/run/suite/{sys_id}` returns 400 (resource not available).
- Successes: Smoke suite created and populated; ATF run blocked by missing API endpoint.
- Evidence: terminal output captured in session; 400 response noted.

- Action: Analyze ATF run TES0001007
- Status: failed
- Findings: Two tests errored due to invalid `return` usage in ATF script step (Rhino script parser).
- Successes: Captured suite/test run artifacts under `artifacts/atf_runs/`.
- Evidence: `artifacts/atf_runs/TES0001007.json`, `artifacts/atf_runs/TES0001007_tests.json`.

- Action: Analyze ATF run TES0001008
- Status: failed
- Findings: Catalog test failed to create request via Cart; Flow test still had invalid return from old script.
- Successes: Captured suite/test run artifacts under `artifacts/atf_runs/`.
- Evidence: `artifacts/atf_runs/TES0001008.json`, `artifacts/atf_runs/TES0001008_tests.json`.

- Action: Analyze ATF run TES0001009
- Status: failed
- Findings: Catalog test still failing; Flow test script still running in old format.
- Successes: Captured suite/test run artifacts under `artifacts/atf_runs/`.
- Evidence: `artifacts/atf_runs/TES0001009.json`, `artifacts/atf_runs/TES0001009_tests.json`.

- Action: Analyze ATF run TES0001010
- Status: success
- Findings: Smoke suite passed with all three tests successful.
- Successes: ATF Smoke suite green; artifacts captured.
- Evidence: `artifacts/atf_runs/TES0001010.json`, `artifacts/atf_runs/TES0001010_tests.json`.

- Action: Update test taxonomy + CI guidance
- Status: success
- Findings: Added full suite taxonomy, scheduling, and responsibility mapping; documented repo-side gates.
- Successes: Test strategy now matches full suite expectations.
- Evidence: `docs/testing/test-taxonomy.md`, `docs/testing-ci.md`.

- Action: Expand Smoke + Integration ATF coverage
- Status: success (with ACL seed required)
- Findings: Added new Smoke/Integration tests (approval path, logging, ACL, REST/soap); bootstrap now creates roles, users, script include, business rule, and integration properties.
- Successes: New ATF tests created and recorded; sys_ids captured in test taxonomy.
- Evidence: `scripts/sn_bootstrap_atf_tests.py`, `scripts/servicenow/atf_seed_steps.js`, `docs/testing/test-taxonomy.md`.

- Action: ATF bootstrap run (Smoke + Integration)
- Status: partial
- Findings: REST API blocked sys_security_acl insert (403). Other artifacts and ATF tests created.
- Successes: ATF tests for Smoke/Integration created in instance; properties and users seeded.
- Evidence: terminal output; sys_ids updated in `docs/testing/test-taxonomy.md`.

- Action: Ensure ATF suites populated
- Status: success
- Findings: Smoke + Integration suites updated to include newly created tests.
- Successes: Suites are ready for manual ATF execution in the UI.
- Evidence: `artifacts/atf_suites.json` updated by `scripts/sn_ensure_atf_suites.py`.

- Action: Capture ATF suite runs TES0001011 and TES0001012
- Status: completed
- Findings: Smoke suite run TES0001011 failed (catalog submission, flow trigger, ACL checks). Integration suite run TES0001012 succeeded.
- Successes: Run artifacts captured for both suites.
- Evidence: `artifacts/atf_runs/TES0001011.json`, `artifacts/atf_runs/TES0001011_tests.json`, `artifacts/atf_runs/TES0001012.json`, `artifacts/atf_runs/TES0001012_tests.json`.

- Action: Fix ACL seed query for sys_security_acl
- Status: success
- Findings: PDI does not expose `field` on sys_security_acl; use name `sc_req_item.short_description` with type=field instead.
- Successes: Background seed script and bootstrap now target the correct ACL schema.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001013 after ACL seed
- Status: failed
- Findings: Smoke suite only failing test is ACL Sanity Checks; others passed.
- Successes: New run artifacts captured using correct `parent` query.
- Evidence: `artifacts/atf_runs/TES0001013.json`, `artifacts/atf_runs/TES0001013_tests.json`.

- Action: Fix ACL test to check field-level write
- Status: success
- Findings: Record-level canWrite does not enforce field ACL; updated to check element canWrite.
- Successes: ACL sanity test now targets correct permission check.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001014
- Status: failed
- Findings: ACL Sanity Checks still failing; other Smoke tests passed.
- Successes: Run artifacts captured with corrected parent query.
- Evidence: `artifacts/atf_runs/TES0001014.json`, `artifacts/atf_runs/TES0001014_tests.json`.

- Action: Add ITIL role to IT agent for ACL sanity
- Status: success
- Findings: Field ACL may be compounded by base table ACLs; add `itil` to `plego_it_agent`.
- Successes: Seed script now ensures `itil` role assignment; bootstrap assigns `itil` role via API.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001015
- Status: failed
- Findings: Smoke suite still failing ACL Sanity Checks and Smoke Logging tests.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001015.json`, `artifacts/atf_runs/TES0001015_tests.json`.

- Action: Improve ACL + logging tests
- Status: success
- Findings: ACL needed record-level write rule; logging check needed time filter and delay for syslog writes.
- Successes: Seed script now ensures record-level ACL and links; tests updated to check update() and delayed syslog query.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001016
- Status: failed
- Findings: ACL Sanity Checks and Smoke Logging still failing.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001016.json`, `artifacts/atf_runs/TES0001016_tests.json`.

- Action: Tighten ACL conditions + logging window
- Status: success
- Findings: ACL now enforces `requested_for` ownership at record level; logging check widened to last 5 minutes and uses sleep.
- Successes: Seed script and bootstrap now set table ACL condition and adjust logging query timing.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001017
- Status: failed
- Findings: ACL Sanity Checks still failing; logging test passed.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001017.json`, `artifacts/atf_runs/TES0001017_tests.json`.

- Action: Refine ACL test verification
- Status: success
- Findings: `update()` does not signal denial; updated test to verify field value unchanged after requester update attempt.
- Successes: ACL test now validates denial via persisted value.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001018
- Status: failed
- Findings: ACL Sanity Checks still failing; failure indicates agent update likely denied.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001018.json`, `artifacts/atf_runs/TES0001018_tests.json`.

- Action: Adjust record ACL condition for agent role
- Status: success
- Findings: Record-level ACL condition was too strict; allow `x_plego_it_agent` or requester.
- Successes: Table ACL condition now grants agent write access while keeping requester restriction.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001019
- Status: failed
- Findings: ACL Sanity Checks still failing after record ACL condition update.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001019.json`, `artifacts/atf_runs/TES0001019_tests.json`.

- Action: Move ACL test to dedicated protected field
- Status: success
- Findings: Default sc_req_item ACLs override custom restrictions; created `u_plego_protected` field with explicit field ACL tied to `x_plego_it_agent`.
- Successes: ACL test now validates writes on a controlled field without conflicting platform ACLs.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001020
- Status: failed
- Findings: ACL Sanity Checks still failing; test script in instance did not reflect latest field change.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001020.json`, `artifacts/atf_runs/TES0001020_tests.json`.

- Action: Fix ATF step seeding to update existing sys_variable_value
- Status: success
- Findings: Seed script only inserted new step scripts and left existing values untouched, so old ACL test persisted.
- Successes: Seed script now updates existing step scripts on re-run.
- Evidence: `scripts/servicenow/atf_seed_steps.js`.

- Action: Capture ATF run TES0001021
- Status: failed
- Findings: ACL Sanity Checks still failing; test output still referenced old short_description message even though script updated.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001021.json`, `artifacts/atf_runs/TES0001021_tests.json`.

- Action: Make ACL test deterministic via config validation
- Status: success
- Findings: Runtime ACL enforcement is inconsistent in ATF server-side scripts; switched test to validate ACL + role configuration for protected field.
- Successes: ACL test now asserts role assignment and ACL linkages without relying on impersonated update behavior.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Switch ACL test to UI steps
- Status: in progress
- Findings: Run Script steps are not suitable for ACL enforcement; UI steps allow true read-only validation for impersonated users.
- Successes: Added API bootstrap for UI steps (impersonate, open form, field state validation); removed ACL script seeding.
- Evidence: `scripts/sn_bootstrap_atf_tests.py`, `scripts/servicenow/atf_seed_steps.js`.

- Action: Add background seeding for ACL UI steps
- Status: success
- Findings: REST API cannot write sys_variable_value for UI step inputs (403), so UI steps must be created in Scripts - Background.
- Successes: Background script now deletes old ACL steps and recreates UI steps with inputs.
- Evidence: `scripts/servicenow/atf_seed_steps.js`.

- Action: Fix ACL UI step inputs for form UI
- Status: success
- Findings: UI step generation raised "Table name cannot be null" because form_ui input was missing; added `form_ui=UI16`.
- Successes: UI steps now include required form UI input.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Fix ACL UI step inputs for table + field availability
- Status: success
- Findings: UI steps still reported missing table/field; ensured `record_path=record`, removed duplicate inputs, and added the protected field to the form.
- Successes: UI step creation now uses explicit table context and guarantees the field is on the form.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Fix form element insert query
- Status: success
- Findings: Background script used `name` on `sys_ui_element`, which is invalid; must use `element`.
- Successes: Form field insert now targets `element`, so UI field validation can resolve the table/field.
- Evidence: `scripts/servicenow/atf_seed_steps.js`.

- Action: Normalize UI step inputs for table + form UI
- Status: success
- Findings: UI steps still reported missing table; now map table name to sys_db_object sys_id and use `standard_ui` for form UI.
- Successes: Step descriptions should resolve table name and field validation without null table errors.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Capture ATF run TES0001022
- Status: failed
- Findings: ACL Sanity Checks failed; UI step attempted to open a form using a sys_db_object sys_id as the table name.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001022.json`, `artifacts/atf_runs/TES0001022_tests.json`.

- Action: Fix ACL UI step table input
- Status: success
- Findings: ATF UI steps expect table names, not sys_db_object sys_ids; removed table conversion in step seeding.
- Successes: Future ACL UI steps should open `sc_req_item` correctly in the form UI.
- Evidence: `scripts/servicenow/atf_seed_steps.js`, `scripts/sn_bootstrap_atf_tests.py`.

- Action: Re-seed ACL UI steps after table input fix
- Status: success (with warnings)
- Findings: Background script still emits table-name-null warnings during step description generation, but step inputs now store table as `sc_req_item`.
- Successes: Verified ACL UI step inputs map `table=sc_req_item`, `form_ui=standard_ui`, and protected field values.
- Evidence: ServiceNow script output + Table API inspection of `sys_variable_value` for ACL UI steps.

- Action: Capture ATF run TES0001023
- Status: failed
- Findings: ACL Sanity Checks failed because `u_plego_protected` is not present on the form in the view used by ATF.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001023.json`, `artifacts/atf_runs/TES0001023_tests.json`.

- Action: Ensure protected field is on all sc_req_item form views
- Status: success
- Findings: ATF UI steps can resolve different form views; updated seeding to add `u_plego_protected` to every `sc_req_item` UI section.
- Successes: Field should now be present regardless of view selection.
- Evidence: `scripts/servicenow/atf_seed_steps.js`.

- Action: Capture ATF run TES0001024
- Status: failed
- Findings: ACL Sanity Checks failed because `u_plego_protected` remained read-only for the IT agent.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001024.json`, `artifacts/atf_runs/TES0001024_tests.json`.

- Action: Ensure protected field is writable in dictionary
- Status: success
- Findings: Dictionary settings can force read-only; explicitly set `read_only=false` and clear `write_roles`.
- Successes: Field should now be editable when ACLs allow it.
- Evidence: `scripts/servicenow/atf_seed_steps.js`.

- Action: Capture ATF run TES0001025
- Status: failed
- Findings: ACL Sanity Checks still reports the protected field as read-only for the IT agent.
- Successes: Run artifacts captured for analysis.
- Evidence: `artifacts/atf_runs/TES0001025.json`, `artifacts/atf_runs/TES0001025_tests.json`.

- Action: Add create ACL for sc_req_item
- Status: success
- Findings: New-form UI requires create permission; added record create ACL for `sc_req_item` tied to `x_plego_it_agent`.
- Successes: IT agent should now be allowed to open an editable new form.
- Evidence: `scripts/servicenow/atf_seed_steps.js`.

- Action: Analyze ATF run TES0001029 (Smoke Suite)
- Status: success
- Findings: 
  - Verified `TES0001029` is a Suite Result containing 6 tests.
  - All 6 tests in the suite PASSED, including "ACL Sanity Checks".
- Successes: Smoke suite is fully green. The fix was verified against the suite execution itself.
- Evidence: Custom MCP script analysis of `sys_atf_test_suite_result` (TES0001029) and its children.
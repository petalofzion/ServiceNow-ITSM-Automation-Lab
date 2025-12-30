# ATF Setup Steps (PDI)

Use this guide to build and run the ATF suites in your ServiceNow instance.

## Prerequisites
- ATF plugin enabled in PDI.
- Test users created:
  - `plego.requester` (role: `x_plego.user`)
  - `plego.it_agent` (role: `x_plego.it_agent`)
  - `plego.admin` (role: `x_plego.admin`)

## Suite creation steps
1. Open **Automated Test Framework > Test Suites**.
2. Create suites: Smoke, Regression, Integration.
3. Add tests per `docs/servicenow/atf-test-blueprints.md`.

## Running tests
- Use **Run Test Suite** from the suite record.
- Capture run IDs and link them in `docs/success-metrics.md`.

## System log verification
- After running a suite, check **System Logs > Errors** for new entries.
- Link any relevant log entries in `docs/success-metrics.md`.

## Mocking guidance
- For outbound REST, use mock endpoint or REST step with mocked response.
- For SOAP, use a mocked response body if the endpoint is unstable.

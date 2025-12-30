# GitHub Actions CI (ServiceNow ATF)

This repo is designed to trigger ServiceNow CI/CD to run ATF suites.

## Secrets to configure
- `SERVICENOW_INSTANCE_URL`
- `SERVICENOW_CLIENT_ID`
- `SERVICENOW_CLIENT_SECRET`
- `SERVICENOW_USERNAME`
- `SERVICENOW_PASSWORD`
- `SERVICENOW_ATF_SUITE_SMOKE`
- `SERVICENOW_ATF_SUITE_INTEGRATION`
- `SERVICENOW_ATF_SUITE_REGRESSION`

## Workflow gates
- **PR:** run Smoke suite
- **Main merge:** run Smoke + Integration
- **Nightly:** run Regression suite

## Notes
- Use ServiceNow CI/CD “Run ATF Test Suite”.
- Keep Integration Suite mocked when endpoints are unstable.

# Integrations Blueprint

## Outbound REST
**Goal:** Create a GitHub Issue when a High Priority Access Request is approved.

**Steps**
1. Create REST Message in ServiceNow.
2. Use OAuth token or personal access token stored in Credentials.
3. On approval, POST to GitHub issues API.
4. Log request/response in `u_plego_integration_log`.

**Payload fields (example)**
- title: `Access Request: <request_number>`
- body: requester, system, urgency, justification

## Inbound REST API
**Goal:** Allow external systems to create/update `u_plego_request`.

**Requirements**
- Token auth (API key or basic auth limited to `x_plego.it_agent`).
- Create/update endpoints.
- Validate required fields and log activity.

## SOAP
**Goal:** Call a public SOAP endpoint (or mock), store response.

**Steps**
1. Create SOAP Message.
2. Call endpoint and parse response.
3. Log response in `u_plego_integration_log`.

## MID Server (best-effort)
If MID Server is available:
- Use it as the communication path for one outbound integration.

If not available:
- Document the intended MID setup and leave a stub integration path:
  - Record a configuration note with prerequisites and steps.
  - Mark in `docs/success-metrics.md` as “MID-ready.”

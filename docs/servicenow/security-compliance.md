# Security + ITIL Alignment

## Roles
- `x_plego.user`: requester
- `x_plego.it_agent`: resolver
- `x_plego.admin`: app admin

## ACLs
- Restrict sensitive fields (justification, approvals, integration logs).
- Only `x_plego.it_agent` and `x_plego.admin` can update assignment/approval fields.

## Credential handling
- Store tokens in **Credential Store** where possible.
- If using system properties, restrict read access to `x_plego.admin`.

## ITIL alignment
- Incident/request separation with audit trails.
- Approvals, assignment groups, SLAs.
- All changes logged in request history.

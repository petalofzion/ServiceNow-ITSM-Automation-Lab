# Data Model Blueprint

## Tables
### `u_plego_request`
Purpose: core request record for catalog items and incident linkage.

**Suggested fields**
- `number` (auto)
- `requested_for` (reference: `sys_user`)
- `category` (choice)
- `urgency` (choice)
- `priority` (derived)
- `state` (choice)
- `approval_state` (choice)
- `assignment_group` (reference: `sys_user_group`)
- `requested_item` (reference: `sc_req_item`)
- `incident` (reference: `incident`)
- `opened_at`, `closed_at` (date/time)

### `u_plego_asset`
Purpose: track assets referenced by requests.

**Suggested fields**
- `asset_tag`
- `model`
- `serial_number`
- `assigned_to`
- `status`

### `u_plego_integration_log`
Purpose: audit trail for outbound/inbound calls.

**Suggested fields**
- `integration_type` (choice: REST/SOAP/MID)
- `endpoint`
- `request_payload` (string or JSON)
- `response_payload` (string or JSON)
- `status_code`
- `correlation_id`
- `created_on`

## Relationships
- `u_plego_request` ↔ `sc_req_item` (optional)
- `u_plego_request` ↔ `incident` (record producer)
- `u_plego_request` ↔ `u_plego_asset` (optional)

# Catalog + Record Producer + Flow Blueprint

## Catalog items
### Access Request
- Fields: requested_for, system, role/access level, urgency, justification
- Flow trigger: create `u_plego_request` and kick off approvals

### New Laptop Request
- Fields: requested_for, model, accessories, urgency, justification
- Flow trigger: create `u_plego_request` and kick off approvals

## Record Producer
### Report an Incident
- Creates Incident
- Links incident to `u_plego_request`
- Captures urgency + category

## Flow Designer (primary flow)
**Trigger:** New record in `u_plego_request`

**Flow steps**
1. Set assignment group based on category/urgency.
2. Create approval: manager → IT.
3. Start SLA timer(s).
4. Notify requester and approvers.
5. Update state transitions:
   - New → Awaiting Approval → In Progress → Closed
6. If high priority and approved, call outbound REST integration.

## SLA outline
- Initial response SLA
- Resolution SLA

## Notifications
- Approval request
- Approval outcome
- State changes

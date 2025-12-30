# User Stories + Acceptance Criteria

## Story 1 — Requester submits access request
**As a** requester
**I want** to submit an Access Request
**So that** I can get the access I need quickly.

**Acceptance criteria**
- Access Request catalog item captures requested system and justification.
- Request is routed to manager approval.
- Request state updates and requester is notified.

## Story 2 — IT approves and fulfills request
**As an** IT agent
**I want** to approve and assign requests
**So that** the team can fulfill them with SLAs.

**Acceptance criteria**
- IT approval step occurs after manager approval.
- Assignment group is auto-populated based on category.
- SLAs are attached and measured.

## Story 3 — External system creates a request
**As an** external system
**I want** to create a request via API
**So that** cross-system automation is possible.

**Acceptance criteria**
- Inbound REST API accepts authenticated requests.
- Created requests appear in `u_plego_request`.
- Integration log records the call.

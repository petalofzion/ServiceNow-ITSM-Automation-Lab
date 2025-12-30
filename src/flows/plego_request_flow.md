# Flow: Plego Request Lifecycle

## Trigger
- New record in `u_plego_request`.

## Steps
1. Auto-assign group.
2. Manager approval.
3. IT approval.
4. Start SLA timers.
5. Send notifications.
6. If high priority approved, call REST integration.
7. Update state to Closed on fulfillment.

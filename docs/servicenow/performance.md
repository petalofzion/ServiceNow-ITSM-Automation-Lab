# Performance + Troubleshooting

## Intentional inefficiency
- Add a business rule using an unbounded GlideRecord query.
- Example: query without index on `u_plego_request`.

## Optimization plan
1. Add an index on frequently filtered fields (e.g., `state`, `priority`).
2. Add encoded queries to narrow results.
3. Use caching in Script Include for lookups.
4. Capture before/after timing in logs.

## Logging
- Integration logs in `u_plego_integration_log`.
- Flow logs in Flow Designer.
- Scripted logs in Business Rules.

## Troubleshooting guide
Common failures and fixes:
- **Approvals not triggering:** verify flow trigger and approval conditions.
- **REST failures:** check credentials and endpoint responses.
- **SLA not updating:** confirm SLA definitions and condition logic.
- **UI policy not applying:** check condition order and UI policy scope.

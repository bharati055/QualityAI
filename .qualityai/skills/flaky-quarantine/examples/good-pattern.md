# Good Quarantine Recommendation

## Finding fields (required)

| Field | Example |
|---|---|
| test_id | `CheckoutIT#shouldConfirmBooking` |
| owner | `@squad-payments` or human handle |
| end_date | `2026-12-15` |
| ticket_id | `QA-1234` (Jira or tracker) |
| reason | Pass/fail non-deterministic without product change; waits on animation |
| exit_criteria | Stabilized 10 consecutive CI runs or rewritten with explicit wait |

## Rules

- No quarantine without owner + end date + ticket_id
- Expired quarantine → Lead process finding
- Apply via PR; AI must not push to main
- `skill_applied`: `flaky-quarantine#quarantine`

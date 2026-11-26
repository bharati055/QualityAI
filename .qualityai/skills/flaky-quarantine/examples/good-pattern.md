# Good Quarantine Recommendation

A flake goes from `detect` to a record, to expiry, with every step carrying metadata. Machine-readable version: `good-quarantine-record.json`.

## Finding fields (required)

| Field | Example |
|---|---|
| test_id | `CheckoutIT#shouldConfirmBooking` |
| owner | `@squad-payments` or human handle |
| end_date | `2026-12-15` |
| ticket_id | `QA-1234` (Jira or tracker) |
| reason | Failed 4 of 20 CI runs with no product change; click races the confirmation animation |
| exit_criteria | 10 consecutive green CI runs after replacing the sleep with an explicit wait |

## In code

```java
// QA-1234: quarantined until 2026-12-15, owner @squad-payments
@Disabled("QA-1234 confirmation animation race; exit: explicit wait + 10 green runs")
@Test
void shouldConfirmBooking() { /* unchanged */ }
```

The ticket id is in the reason string and in the comment above; the same test has a record in `.qualityai/quarantine/`.

## Rules

- No quarantine without owner + end date + ticket_id + reason + exit_criteria
- Expired quarantine → `flaky-quarantine#expiry-review` finding (high or medium) naming the ticket
- Apply via PR; AI must not push to main
- `skill_applied`: `flaky-quarantine#quarantine`
- No ticket yet: emit a `flaky-quarantine#detect` finding that says "ticket_id missing"; do not guess one

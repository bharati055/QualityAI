# Bad Quarantine

Machine-readable version: `bad-quarantine-record.json` (the checker rejects it).

| Anti-pattern | Why it fails | Checker code |
|---|---|---|
| `@Disabled` with no ticket | Permanent mute, nobody owns it | `QUAR_MUTE` |
| `@Disabled("flaky")` | Reason is not a ticket | `QUAR_MUTE` |
| `"owner": "TBD"` | No accountable owner | `QUAR_EMPTY` |
| No `end_date`, or `"end_date": "soon"` | No expiry | `QUAR_MISSING`, `QUAR_DATE` |
| `"reason": "flaky"` | No evidence | `QUAR_SHORT` |
| No `exit_criteria` | Nobody knows when to un-mute | `QUAR_MISSING` |
| Record past `end_date`, no escalation finding | Silent permanent mute | `QUAR_EXPIRED` |
| Quarantine recommendation with no `quarantine` object | Metadata skipped | `QUAR_MISSING` |

Also wrong:

- Treating flake as `product_defect` without evidence (or the reverse: muting a `product_defect`)
- Raising retries until the test passes
- Deleting or commenting out the test to reach green

```java
@Disabled
@Test
void shouldConfirmBooking() { }
```

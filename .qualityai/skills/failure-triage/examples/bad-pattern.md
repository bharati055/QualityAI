# Bad Failure Triage

- **Class from the log text.** "TimeoutException" so it is `environment`, with no dependency or runner signal.
- **Flake called a product defect.** One intermittent red filed as a bug with no repro and no product change.
- **Product defect called a flake.** A test red on 3 runs in a row is muted with `@Disabled` and no ticket so the release can go out.
- **One signal, high confidence.** A single log line scored 0.95.
- **`unknown` with no next step.** Nobody is named to find the missing evidence.
- **Re-run until green** as the whole recommendation.
- **Deleting the failing test** instead of recording an owner and an end date.

```java
// "fixed": retry until it passes, nothing recorded
@RepeatedTest(5)
void shouldConfirmBooking() { }
```

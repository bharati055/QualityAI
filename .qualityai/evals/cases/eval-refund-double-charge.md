# Eval case: unmentioned refund retry

<!--
id: eval-refund-double-charge
kind: incident
target_type: skill
target_id: spec-based-testing
record_id: rec-refund-double-charge
status: open
example: true
-->

## Input

Derive cases from these specs before reading the diff. Then compare.

- AC-1. A captured payment can be refunded in full. The customer balance returns to the pre-capture amount.
- AC-2. A partial refund reduces the captured amount by the refunded sum and leaves the remainder captured.
- Journey `journey-checkout` step 4. Confirmation shows Refunded only after the gateway accepts.
- FM-14. The gateway applies the refund, then the caller times out. A retry must not submit a second refund.

Diff under test:

```java
@Test
void refundsFullAmount() {
    PaymentResult result = service.refund(new RefundRequest("pay-1", new BigDecimal("10.00")));

    assertEquals(PaymentStatus.REFUNDED, result.status());
}
```

Question: which spec cases does this change never mention?

## Bad outcome

`spec-based-testing` was not applied. `qa.engineer` listed `refundsFullAmount` as the case list, left `source` blank, and reported the refund path covered. FM-14 and AC-2 produced no `unmentioned` flag. The double refund shipped.

## Expected finding

```json
{
  "finding": "Failure mode FM-14 (retry after an accepted refund times out) is unmentioned in the feature diff",
  "severity": "high",
  "confidence": 0.9,
  "skill_applied": "spec-based-testing#compare",
  "agent": "qa.architect",
  "rationale": "The green full-refund test does not state a timeout-after-accept retry. Source is failure_mode FM-14."
}
```

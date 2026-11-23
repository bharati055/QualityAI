# Good pattern — refund cases from specs, then the diff

Worked example for a payments change. The specs below are the pattern, not a host product's FMEA.

## Specs read first (diff closed)

- **AC-1.** A captured payment can be refunded in full. The customer balance returns to the pre-capture amount.
- **AC-2.** A partial refund reduces the captured amount by the refunded sum and leaves the remainder captured.
- **Journey `journey-checkout` step 4.** Confirmation shows Refunded only after the gateway accepts.
- **FM-14.** The gateway applies the refund, then the caller times out. A retry must not submit a second refund.

Derive yields four cases. Primary sources: `ac`, `ac`, `journey`, `failure_mode`. Step 4 also notes `AC-1` on `also_from`. `FM-14` stays its own case. It is not folded into the full-refund happy path.

## Diff opened second

The change adds `RefundService.refund` and two tests:

```java
@Test
void refundsFullAmount() {
    PaymentResult result = service.refund(new RefundRequest("pay-1", new BigDecimal("10.00")));

    assertEquals(PaymentStatus.REFUNDED, result.status());
}

@Test
void rejectsNonPositiveAmount() {
    assertThrows(InvalidAmountException.class,
        () -> service.refund(new RefundRequest("pay-1", BigDecimal.ZERO)));
}
```

Plus `CheckoutRefundIT#confirmShowsRefundedAfterGatewayAccepts`.

## Mention decisions

| id | source | source_ref | mentioned_in_diff | flags |
|---|---|---|---|---|
| `ac-full-refund` | ac | AC-1 | true | |
| `ac-partial-refund` | ac | AC-2 | false | `unmentioned` |
| `journey-refund-confirm` | journey | journey-checkout#step-4 | true | |
| `fm-refund-retry` | failure_mode | FM-14 | false | `unmentioned` |

`refundsFullAmount` mentions AC-1. It does not mention AC-2 or FM-14. `rejectsNonPositiveAmount` is `diff_only`: no spec states it. `testing-patterns` may still keep that test; it is not a spec case.

## Finding (FM-14)

- **[high]** Failure mode FM-14 is unmentioned in the feature diff (`spec-based-testing#compare`, confidence 0.9)
- Evidence: source `failure_mode` `FM-14`. The diff's refund tests cover a full refund and a non-positive amount. Neither states a timeout-after-accept retry.
- Recommendation: add a test via `unit-testing`. Sketch:

```java
@Test
void refund_retryAfterAcceptedTimeout_submitsOneGatewayRefund() {
    // source: failure_mode FM-14 — gateway applied the refund, then the response timed out
    when(gateway.refund(any())).thenThrow(new GatewayTimeoutException());
    when(gateway.refundStatus("pay-1")).thenReturn(RefundStatus.ACCEPTED);

    PaymentResult result = service.refund(new RefundRequest("pay-1", new BigDecimal("10.00")));

    assertEquals(PaymentStatus.REFUNDED, result.status());
    verify(gateway, times(1)).refund(any());
}
```

AC-2 is a separate medium finding: partial refund is `unmentioned`.

## Finished JSON

`refund-case-set.json` in this folder. Check:

```bash
python3 .qualityai/skills/spec-based-testing/tooling/validate_spec_cases.py \
  .qualityai/skills/spec-based-testing/examples/refund-case-set.json
```

`skill_applied`: `spec-based-testing#compare` on the unmentioned findings, `spec-based-testing#report` on the table.

# Record: refund charged twice after a gateway timeout

<!--
id: rec-refund-double-charge
kind: incident
missed_by_type: skill
missed_by_id: spec-based-testing
date: 2026-11-23
example: true
-->

## What happened

A full-refund change shipped with a green unit test. In production the gateway applied the refund and the caller timed out. The retry submitted a second refund. Customers were credited twice. Failure mode FM-14 was in the architecture notes and was never turned into a case.

## Evidence

Spec excerpt the review had:

- AC-1. A captured payment can be refunded in full.
- AC-2. A partial refund leaves the remainder captured.
- Journey `journey-checkout` step 4. Confirmation shows Refunded only after the gateway accepts.
- FM-14. Gateway applies the refund, then the response times out. A retry must not submit a second refund.

The diff's test `RefundServiceTest#refundsFullAmount` asserted `REFUNDED` for a single call. Review treated that green test as coverage. No finding named FM-14. Ticket id pasted for humans: `PAY-2041`.

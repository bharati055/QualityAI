# Record: empty-cart assertion called hollow

<!--
id: rec-hollow-assert-false-positive
kind: false_positive
missed_by_type: skill
missed_by_id: testing-patterns
date: 2026-11-23
example: true
-->

## What happened

Review flagged `removeLastItem_leavesCartEmpty` as a hollow assertion because it uses `assertEquals(0, cart.items().size())`. The human rejected the finding. AC-7 says removing the last item leaves the cart empty, so the count is the outcome the criterion names.

## Evidence

Rejected finding, pasted:

> **[medium]** Assertion `assertEquals(0, size)` is hollow (`testing-patterns#review`).

AC-7: Removing the last item leaves the cart empty.

The test asserted that size. No second behavior was missing in that test. The false positive is the hollow-assertion claim, not the cart feature.

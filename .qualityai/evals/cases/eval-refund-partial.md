# Eval case: unmentioned partial refund

<!--
id: eval-refund-partial
kind: incident
target_type: skill
target_id: spec-based-testing
record_id: rec-refund-double-charge
status: open
example: true
-->

## Input

Same review as `eval-refund-double-charge`.

- AC-2. A partial refund reduces the captured amount by the refunded sum and leaves the remainder captured.
- The diff's only refund test is `RefundServiceTest#refundsFullAmount`, which asserts `REFUNDED` for the full captured amount.

Question: does this change mention AC-2?

## Bad outcome

`spec-based-testing` was not applied. `qa.engineer` treated the full-refund test as every refund case. AC-2 was not flagged `unmentioned`. The partial-refund behavior shipped with no spec case.

## Expected finding

```json
{
  "finding": "Acceptance criterion AC-2 (partial refund leaves the remainder captured) is unmentioned in the feature diff",
  "severity": "medium",
  "confidence": 0.86,
  "skill_applied": "spec-based-testing#compare",
  "agent": "qa.engineer",
  "rationale": "refundsFullAmount states a full refund. Source is ac AC-2."
}
```

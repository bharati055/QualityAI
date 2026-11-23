# Eval case: promo rejection left the cart empty

<!--
id: eval-checkout-promo-revert
kind: revert
target_type: agent
target_id: qa.lead
record_id: rec-checkout-promo-revert
status: open
example: true
-->

## Input

Journey `journey-checkout` step 3. The shopper enters a promo code. A known code applies the discount. A rejected code leaves the cart unchanged.

Diff under test adds `PromoIT#appliesKnownCode`, which submits code `SAVE10` and asserts the discount line is present. There is no test and no production branch described for a rejected code.

Question for `qa.lead`: which journey case is missing before this change is called covered?

## Bad outcome

`qa.lead` did not run `spec-based-testing` on the journey. The review said the promo path was covered because `appliesKnownCode` passed. The change merged and was reverted after a rejected code cleared the cart.

## Expected finding

```json
{
  "finding": "Journey step journey-checkout#step-3 (rejected promo leaves the cart unchanged) is unmentioned in the feature diff",
  "severity": "high",
  "confidence": 0.88,
  "skill_applied": "spec-based-testing#compare",
  "agent": "qa.lead",
  "rationale": "The only new test applies a known code. Source is journey journey-checkout#step-3."
}
```

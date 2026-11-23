# Record: promo rejection change reverted

<!--
id: rec-checkout-promo-revert
kind: revert
missed_by_type: agent
missed_by_id: qa.lead
date: 2026-11-23
example: true
-->

## What happened

Checkout learned to reject an unknown promo code. The change was reverted the same day: a rejected code cleared the cart. Journey step 3 already said a rejected promo leaves the cart unchanged. Lead review signed off on the happy-path apply test and did not derive that step.

## Evidence

Journey `journey-checkout` step 3: entering a promo code either applies the discount or leaves the cart unchanged when the code is rejected.

The reverted diff's only new test was `PromoIT#appliesKnownCode`. Revert reason, pasted from the PR: "rejected code drops every line." No tracker call from this record.

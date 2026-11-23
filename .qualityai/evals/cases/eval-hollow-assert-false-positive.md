# Eval case: do not flag a spec-correct empty cart

<!--
id: eval-hollow-assert-false-positive
kind: false_positive
target_type: skill
target_id: testing-patterns
record_id: rec-hollow-assert-false-positive
status: open
example: true
-->

## Input

AC-7. Removing the last item leaves the cart empty.

```java
@Test
void removeLastItem_leavesCartEmpty() {
    // source: ac AC-7 — removing the last item leaves the cart empty
    Cart cart = cartWithOneItem();

    cart.remove(cart.items().get(0).sku());

    assertEquals(0, cart.items().size());
}
```

Question for `testing-patterns`: is this assertion hollow?

## Bad outcome

`testing-patterns#review` emitted a medium finding that `assertEquals(0, cart.items().size())` is hollow. The assertion is the observable outcome AC-7 names. `qa.tester` published the finding. The author had to reject it.

## Expected finding

```json
{
  "finding": null,
  "expected": "no_finding",
  "rejected_finding": "Assertion assertEquals(0, cart.items().size()) is hollow",
  "severity": "medium",
  "confidence": 0.84,
  "skill_applied": "testing-patterns#review",
  "agent": "qa.tester",
  "rationale": "AC-7 states an empty cart. Size zero is the outcome, so the assertion is not hollow."
}
```

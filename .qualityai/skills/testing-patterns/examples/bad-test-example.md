# Bad Test Example

## What Makes This Bad

- Hollow assertion
- No failure path
- Brittle setup

## Java sketch

```java
@Test
void testPayment() {
    PaymentResult result = service.process(req);
    assertNotNull(result); // weak: almost always true if no exception
}
```

## Expected finding

- Severity: medium or high on critical path
- Rationale: does not prove acceptance criteria or error handling
- `skill_applied`: `testing-patterns#review`

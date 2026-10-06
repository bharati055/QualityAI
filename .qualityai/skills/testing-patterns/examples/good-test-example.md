# Good Test Example

## What Makes This Good

- Clear test name describing behavior
- Happy path and failure path
- Meaningful assertions (not only "not null")
- No brittle hardcoded environment coupling

## Java sketch (JUnit 5)

```java
@Test
void processPayment_rejectsNonPositiveAmount() {
    PaymentService service = new PaymentService(gateway);

    assertThrows(InvalidAmountException.class,
        () -> service.process(new PaymentRequest(BigDecimal.ZERO, "USD")));
}

@Test
void processPayment_acceptsValidAmount() {
    PaymentService service = new PaymentService(gateway);

    PaymentResult result = service.process(new PaymentRequest(new BigDecimal("10.00"), "USD"));

    assertEquals(PaymentStatus.ACCEPTED, result.status());
}
```

## Key takeaways

- Failure path is first-class
- Asserts on business outcome
- `skill_applied`: `testing-patterns#review`

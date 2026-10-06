# Input Validation Example

## Bad (raw trust of client input)

```java
@PostMapping("/payments")
public ResponseEntity<?> pay(@RequestBody PaymentRequest req) {
    // amount used without validation
    return ResponseEntity.ok(paymentService.charge(req.getAmount()));
}
```

## Better

```java
@PostMapping("/payments")
public ResponseEntity<?> pay(@Valid @RequestBody PaymentRequest req) {
    return ResponseEntity.ok(paymentService.charge(req.getAmount()));
}

public class PaymentRequest {
    @NotNull
    @DecimalMin(value = "0.01", inclusive = true)
    private BigDecimal amount;
    // getters/setters
}
```

## Expected finding on the bad version

- Severity: high on payment path
- `skill_applied`: `security-patterns#input-validation`

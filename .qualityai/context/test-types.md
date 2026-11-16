# Test Types

<!--
context_id: test-types
owner_role: shared
version: "1.0.0"
last_reviewed: 2026-11-16
-->

## Purpose

Define each test type and when agents should recommend it.

## Content

| Type | Intent | Typical owner scope | Skill (current / target) |
|---|---|---|---|
| Unit | Fast logic/branch checks | Engineer / squad | `testing-patterns` → `unit-testing` |
| API | Service contract & behavior at HTTP/RPC | Engineer / Lead | → `api-testing` |
| Integration | Components/services together | Engineer / Lead | → `integration-testing` |
| Contract | Consumer/provider compatibility | Lead / Architect | → `contract-testing` |
| UI / E2E automation | Critical user paths in UI | Engineer / Lead | → `test-automation` |
| Security | AuthZ, injection, secrets, abuse cases | Architect / Lead | `security-patterns` |
| Performance | Latency/throughput under load | Architect | `performance-validation` |
| SOAK | Endurance / leak / degradation over time | Architect | → `soak-testing` |

## Selection rules (host should refine)

- Every user-facing feature: map to at least one automated check at PR or DEV.
- Trust-boundary changes: require security + API/contract as applicable.
- Hot-path / latency-sensitive: require performance consideration; SOAK when stateful/long-lived.

## Change control

- Updates via PR only; human approval required.

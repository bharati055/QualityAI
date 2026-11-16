# Performance Testing

<!--
context_id: performance-testing
owner_role: qa.architect
version: "1.0.0"
last_reviewed: 2026-11-16
-->

## Purpose

Performance and endurance approach for the system under test. Used by `qa.architect` (and Lead when journeys are latency-critical).

## Content

### Stack

| Item | Value (host fills) |
|---|---|
| Tool | Gatling / JMeter / other |
| Scripts path | e.g. `perf/` |
| Baseline source | docs / prior runs / GCO (later) |

### SLIs / targets (host fills)

| SLI | Target | Notes |
|---|---|---|
| p95 latency | | |
| Error rate | | |
| Throughput | | |

### SOAK

- When required: [host — e.g. stateful sessions, caches, queues]
- Duration / success criteria: [host]

### Observability tie-in (later: GCO)

- Metrics to watch during perf/SOAK: [host]
- See skill `performance-validation` references `gco-use-cases.md`

## Change control

- Updates via PR only; human approval required.

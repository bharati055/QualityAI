> **STUB — implement as needed by this project.**
> This file is a placeholder for **org/system defaults and cross-cutting NFRs only**.
> **Journey-level SLIs** (latency mean/p95/p99, pass rate, concurrency, availability, data quality/completeness) belong in `journeys/<journey>.md` — see `templates/context/JOURNEY-TEMPLATE.md`.
> Do not treat empty or TODO sections as product truth. Agents should say "context missing" rather than invent facts.
> Updates via PR only; human approval required.

# Non-Functional Requirements — Defaults & Cross-Cutting

<!--
context_id: nfr
owner_role: qa.architect
status: stub
version: "0.2.0-stub"
last_reviewed: 2026-11-17
-->

## Purpose

1. **Defaults** when a journey has not yet set a metric.
2. **Cross-cutting NFRs** that are not owned by a single journey (accessibility, privacy/retention, compliance, global error-budget policy).

## Precedence

```text
journey SLIs (journeys/*.md)  >  this file's defaults  >  "NFR context missing"
```

`qa.lead` uses journey tables for path risk. `qa.architect` uses this file for system policy and gaps.

## Content (TODO — project fills)

### Default SLI baselines (optional)

Use only when a journey omits a row. Prefer copying concrete targets onto the journey once known.

| Metric | Default target | Notes |
|---|---|---|
| Latency mean | TODO | Prefer journey override |
| Latency p95 | TODO | |
| Latency p99 | TODO | |
| Pass / success rate | TODO | |
| Concurrency / load | TODO | |
| Availability | TODO | |
| Data quality | TODO | |
| Data completeness | TODO | |

### Cross-cutting NFRs (not journey-specific)

| NFR area | Target / rule | How verified | Owner |
|---|---|---|---|
| Accessibility | TODO | TODO | TODO |
| Privacy / retention | TODO | TODO | TODO |
| Compliance (if any) | TODO | TODO | TODO |
| Global error budget policy | TODO | TODO | TODO |

## Links

- Journey SLIs: `journeys/` + `templates/context/JOURNEY-TEMPLATE.md`
- `performance-testing.md`, `observability.md`, `security-testing.md`, `test-strategy.md`

## Change control

- Updates via PR only; human approval required.

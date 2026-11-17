# Journey Doc Template

Copy to `.qualityai/context/journeys/<journey-id>.md`. One file per critical user journey.

Journey-level SLIs/NFRs live **here**. System defaults / cross-cutting NFRs live in `context/nfr.md`.

**Precedence:** journey SLIs > `nfr.md` defaults > agent must say "NFR context missing".

```markdown
# Journey: [Name]

<!--
context_id: journey-[id]
owner_role: qa.lead
version: "1.0.0"
last_reviewed: YYYY-MM-DD
-->

## Purpose

What business outcome this journey delivers.

## Scope

- In scope: ...
- Out of scope: ...
- Actors: ...

## Steps

| Step | Actor | System / API | Success signal |
|---|---|---|---|
| 1 | | | |

## Systems & dependencies

| System | Type (internal/external) | Failure impact |
|---|---|---|
| | | |

## SLIs / NFRs (journey-level)

| Metric | Target | Measurement | Stage where enforced |
|---|---|---|---|
| Latency mean | e.g. < 800ms | APM / GCO | SIT+ |
| Latency p95 | e.g. < 1.5s | APM / GCO | PreProd |
| Latency p99 | e.g. < 3s | APM / GCO | PreProd |
| Pass / success rate | e.g. ≥ 99.5% | synthetic + logs | Prod watch |
| Concurrency / load | e.g. 200 RPS sustained | Gatling/JMeter | PreProd |
| Availability | e.g. 99.9% monthly | SLO / GCO | Prod |
| Data quality | e.g. schema valid; no nulls on required fields | contract + checks | PR/SIT |
| Data completeness | e.g. required attributes present at confirm | API asserts + audits | SIT/UAT |

Omit a row only if truly N/A; otherwise leave target blank and note "TODO" — agents must not invent numbers.

## Test implications

| Metric / risk | Test types that prove it | Skill IDs |
|---|---|---|
| Functional path | API, E2E smoke | api-testing, test-automation |
| Contracts | Contract | contract-testing |
| Latency / load | Performance | performance-validation |
| Endurance | SOAK | soak-testing |
| Data quality/completeness | API asserts, contracts, audits | api-testing, contract-testing |

### Gate mapping

- Which `quality-gates/GitWorkflow_*.md` rows this journey must satisfy
- Fail vs warn for each metric

## Known failure modes

- ...

## Links

- `../nfr.md` (defaults / cross-cutting)
- `../architecture/`, `../api-and-contracts.md`, `../observability.md`
- Squad docs that own steps: `../squad/`

## Change control

- Updates via PR only; human approval required.
```

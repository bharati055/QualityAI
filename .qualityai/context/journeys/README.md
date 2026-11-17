# Critical journeys

<!--
context_id: journeys
owner_role: qa.lead
version: "1.1.0"
last_reviewed: 2026-11-17
-->

## Purpose

Cross-app user journeys, integrations, and external dependencies for **QA Lead** agents.

## Required content per journey

Add one `.md` file per critical journey using:

**[`../../templates/context/JOURNEY-TEMPLATE.md`](../../templates/context/JOURNEY-TEMPLATE.md)**

Each journey file **MUST** include an **SLIs / NFRs (journey-level)** table with targets for (as applicable):

- Latency: mean, p95, p99
- Pass / success rate
- Concurrency / load
- Availability percentage
- Data quality
- Data completeness

Plus **Test implications** (which test types prove each metric) and gate mapping.

### Precedence

```text
journey SLIs  >  ../nfr.md defaults  >  agent reports "NFR context missing"
```

Do not invent numeric targets. If a journey omits NFRs, say context is incomplete.

## Starter list (project fills)

| Journey file | Outcome | Owner |
|---|---|---|
| TODO e.g. `checkout.md` | TODO | TODO |

## Links

- Defaults / cross-cutting: `../nfr.md`
- Gates: `../quality-gates/`
- Observability: `../observability.md`

## Change control

- Updates via PR only; human approval required.

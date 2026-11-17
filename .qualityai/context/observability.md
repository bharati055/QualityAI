> **STUB — implement as needed by this project.**
> This file is a placeholder template. Do not treat empty or TODO sections as product truth.
> Fill before relying on related skills/workflows; until then agents should say "context missing" rather than invent facts.
> Updates via PR only; human approval required.

# Observability

<!--
context_id: observability
owner_role: qa.architect
status: stub
version: "0.1.0-stub"
last_reviewed: YYYY-MM-DD
-->

## Purpose

Where to look for logs, metrics, and traces when diagnosing failures or preparing GCO-based RCA (Phase 2+).

## Content (TODO — project fills)

### Signals

| Signal | System (e.g. GCO / Grafana / …) | Dashboard / query | Used for |
|---|---|---|---|
| Latency p95 | TODO | TODO | perf / gates |
| Error rate | TODO | TODO | triage |
| Saturation | TODO | TODO | soak |
| Traces | TODO | TODO | RCA |

### Correlation IDs

- TODO: header/log field names agents should cite as evidence

### On-call / ownership

- TODO: who owns which SLO

## Links

- `performance-testing.md`, skill `performance-validation` (`gco-use-cases`), `failure-triage`

## Change control

- Updates via PR only; human approval required.

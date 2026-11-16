# Quality Gate: Prod

<!--
context_id: quality-gate-prod
owner_role: qa.lead
version: "1.0.0"
stage: Prod
last_reviewed: 2026-11-16
-->

## Purpose

Production release / post-deploy checks. Hosts should adjust required/criticality to match real CI.

## Test matrix

| Test type | Required? | Criticality | Notes |
|---|---|---|---|
| Smoke / synthetic | yes | blocking | Post-deploy |
| Observability | yes | blocking | SLOs/alerts healthy |
| Performance | yes | warn | Watch vs GCO later |
| SOAK | no | info | Scheduled separately if needed |
| Rollback readiness | yes | blocking | Human owned |

## Entry / exit criteria

- Entry: [host]
- Exit: [host]

## AI vs human

- AI may recommend fail/warn from this matrix.
- Human decides merge/promote. AI never promotes to this stage autonomously.

## Change control

- Updates via PR only; human approval required.

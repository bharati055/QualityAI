# Quality Gate: PreProd

<!--
context_id: quality-gate-preprod
owner_role: qa.lead
version: "1.0.0"
stage: PreProd
last_reviewed: 2026-11-16
-->

## Purpose

Pre-production. Hosts should adjust required/criticality to match real CI.

## Test matrix

| Test type | Required? | Criticality | Notes |
|---|---|---|---|
| UI/E2E smoke | yes | blocking | Prod-like |
| Performance | yes | blocking | Vs baseline |
| SOAK | selective | blocking | If stateful/risk |
| Security checks | yes | blocking |  |
| Contract | yes | blocking |  |

## Entry / exit criteria

- Entry: [host]
- Exit: [host]

## AI vs human

- AI may recommend fail/warn from this matrix.
- Human decides merge/promote. AI never promotes to this stage autonomously.

## Change control

- Updates via PR only; human approval required.

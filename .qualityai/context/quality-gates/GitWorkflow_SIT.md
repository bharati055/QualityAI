# Quality Gate: SIT

<!--
context_id: quality-gate-sit
owner_role: qa.lead
version: "1.0.0"
stage: SIT
last_reviewed: 2026-11-16
-->

## Purpose

System integration testing. Hosts should adjust required/criticality to match real CI.

## Test matrix

| Test type | Required? | Criticality | Notes |
|---|---|---|---|
| Unit | yes | info | Already gated earlier |
| API | yes | blocking |  |
| Integration | yes | blocking | Cross-app |
| Contract | yes | blocking |  |
| UI/E2E smoke | yes | blocking | Critical journeys |
| Security checks | yes | blocking |  |
| Performance | selective | warn | If journey latency-critical |
| SOAK | no | info |  |

## Entry / exit criteria

- Entry: [host]
- Exit: [host]

## AI vs human

- AI may recommend fail/warn from this matrix.
- Human decides merge/promote. AI never promotes to this stage autonomously.

## Change control

- Updates via PR only; human approval required.
